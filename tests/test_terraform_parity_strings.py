#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Terraform parity for the string and type-conversion functions.

Every expectation here was measured on 2026-08-17, and the command that produced
it is quoted beside it. Two oracles were needed:

* `soup-go cty call <function> <arg-json>...` -- real go-cty, which is what
  Terraform registers for `upper`, `lower`, `format`, `join`, `split` and
  `tostring`.
* `terraform console` (Terraform 1.14.0) -- needed for `replace`, because
  Terraform does *not* register go-cty's `stdlib.Replace`. It substitutes its own
  regex-aware version, and the harness measurably disagrees: go-cty answers
  `"hello world"` for `replace("hello world", "/w.*d/", "x")` where Terraform
  answers `"hello x"`.

Neither oracle is invoked from here: they live outside this repo and these
functions are pure, so the measured answers are pinned as literals and the sweep
that produced them stays reproducible from the quoted commands.

The null -> null policy these functions carry is deliberately *not* Terraform's
and is pinned in `test_tdd_stdlib_functions.py` / `test_tdd_function_semantics.py`
instead; nothing here contradicts it.
"""

import pytest
from pyvider.exceptions import FunctionError

from pyvider.components.functions.string_manipulation import (
    format_str,
    join,
    lower,
    replace,
    split,
    upper,
)
from pyvider.components.functions.type_conversion_functions import tostring

TWO_CAPITAL_SIGMA = "ΣΣ"
"""GREEK CAPITAL LETTER SIGMA, twice."""

TWO_SMALL_SIGMA = "\u03c3\u03c3"
"""GREEK SMALL LETTER SIGMA, twice: Go's answer for `lower` of the above.

Escaped rather than written literally because a lone lowercase sigma is
confusable with a Latin `o`, which is exactly the kind of thing that should not
be decided by eye in a test that pins Unicode behaviour.
"""

SIGMA_THEN_FINAL_SIGMA = "\u03c3\u03c2"
"""GREEK SMALL LETTER SIGMA then FINAL SIGMA: Python's answer, from a rule Go has not."""

DOTTED_CAPITAL_I = "İ"
"""LATIN CAPITAL LETTER I WITH DOT ABOVE, whose full lowercase is two code points."""

I_WITH_COMBINING_DOT = "i̇"
"""Python's full lowercase of the above: `i` plus COMBINING DOT ABOVE."""

FI_LIGATURE = "ﬁ"
"""LATIN SMALL LIGATURE FI, whose full uppercase is the two letters `FI`."""

ALPHA_YPOGEGRAMMENI = "ᾀ"
"""GREEK SMALL LETTER ALPHA WITH PSILI AND YPOGEGRAMMENI."""

ALPHA_PROSGEGRAMMENI = "ᾈ"
"""Its *simple* uppercase, a single code point; the full mapping gives two."""


class TestCaseMappingIsGoSimpleMapping:
    """`upper`/`lower` map one code point at a time, as Go's `strings` package does.

    Measured, with the Greek and Turkish arguments spelled by name above:

        soup-go cty call upper '{"type":"string","value":"straße"}'   -> "STRAßE"
        soup-go cty call upper '{"type":"string","value":"<FI>"}'     -> "<FI>"
        soup-go cty call lower '{"type":"string","value":"<2xSIGMA>"}' -> "<2x small sigma>"
        soup-go cty call lower '{"type":"string","value":"<I-dot>"}'  -> "i"

    Python's `str.upper()`/`str.lower()` answered "STRASSE", "FI", sigma +
    final-sigma and `i` + COMBINING DOT ABOVE for the same four, because they
    apply `SpecialCasing.txt`'s full mapping plus the context-sensitive
    final-sigma rule. Go implements neither.
    """

    @pytest.mark.parametrize(
        ("value", "expected", "python_answer"),
        [
            ("straße", "STRAßE", "STRASSE"),
            (FI_LIGATURE, FI_LIGATURE, "FI"),
            ("hello world", "HELLO WORLD", "HELLO WORLD"),
        ],
    )
    def test_upper_uses_simple_mapping(self, value, expected, python_answer):
        assert upper(value) == expected
        if expected != python_answer:
            assert value.upper() == python_answer, "the divergence this pins has moved"

    @pytest.mark.parametrize(
        ("value", "expected", "python_answer"),
        [
            (TWO_CAPITAL_SIGMA, TWO_SMALL_SIGMA, SIGMA_THEN_FINAL_SIGMA),
            (DOTTED_CAPITAL_I, "i", I_WITH_COMBINING_DOT),
            ("HELLO", "hello", "hello"),
        ],
    )
    def test_lower_uses_simple_mapping(self, value, expected, python_answer):
        assert lower(value) == expected
        if expected != python_answer:
            assert value.lower() == python_answer, "the divergence this pins has moved"

    def test_simple_mapping_never_changes_length(self):
        """A simple mapping is one code point in, one code point out.

        The property that separates it from Python's: `"ß".upper()` is two code
        points, and a string that grows under `upper` is the shape of the bug.
        """
        sample = f"straße {FI_LIGATURE} {TWO_CAPITAL_SIGMA} {DOTTED_CAPITAL_I} {ALPHA_YPOGEGRAMMENI} ŉ"
        assert len(upper(sample)) == len(sample)
        assert len(lower(sample)) == len(sample)

    def test_upper_of_greek_ypogegrammeni_is_the_prosgegrammeni_form(self):
        """U+1F80's simple uppercase is a single code point, U+1F88.

            soup-go cty call upper '{"type":"string","value":"<U+1F80>"}'  -> "<U+1F88>"

        The naive "keep the character when the full mapping lengthens it" fix
        answers U+1F80 here, so this is the case that rules that fix out: the
        full mapping gives U+1F08 U+0399, two code points, neither of them the
        simple answer.
        """
        assert upper(ALPHA_YPOGEGRAMMENI) == ALPHA_PROSGEGRAMMENI
        assert ALPHA_YPOGEGRAMMENI.upper() == "ἈΙ"


class TestFormatPrintfVerbs:
    """`format`'s printf verbs, which used to reach state as literal text.

    Measured, each as `soup-go cty call format <template> <value>...`:

        "%.2f"        3.14159   -> "3.14"
        "%5s"         "a"       -> "    a"
        "%-10s|"      "a"       -> "a         |"
        "%08.3f"      3.14159   -> "0003.142"
        "%x"          255       -> "ff"
        "%q"          "a"       -> "\\"a\\""
        "%v"          "a"       -> "a"
        "%t"          true      -> "true"
        "%b"          5         -> "101"
        "%o"          8         -> "10"
        "%e"          1234.5678 -> "1.234568e+03"
        "100%%"       (none)    -> "100%"
        "%[1]s %[1]s" "a"       -> "a a"

    Before 2026-08-17 the dispatch was `re.search(r"%[sdfrg]", template)`, which
    matches only a bare verb. Every one of these missed it, fell through to
    `str.format()`, and was returned unchanged with no error at all.
    """

    @pytest.mark.parametrize(
        ("template", "values", "expected"),
        [
            ("%.2f", [3.14159], "3.14"),
            ("%5s", ["a"], "    a"),
            ("%-10s|", ["a"], "a         |"),
            ("%08.3f", [3.14159], "0003.142"),
            ("%x", [255], "ff"),
            ("%q", ["a"], '"a"'),
            ("%v", ["a"], "a"),
            ("%t", [True], "true"),
            ("%b", [5], "101"),
            ("%o", [8], "10"),
            ("%e", [1234.5678], "1.234568e+03"),
            ("100%%", [], "100%"),
            ("%[1]s %[1]s", ["a"], "a a"),
            # soup-go cty call format '{"type":"string","value":"%5.2f|%-6d|"}' ...
            ("%5.2f|%-6d|", [3.14159, 42], " 3.14|42    |"),
            # soup-go cty call format '{"type":"string","value":"%v"}'
            #   '{"type":["tuple",["number","number"]],"value":[1,2]}'
            ("%v", [[1, 2]], "[1,2]"),
        ],
    )
    def test_printf_verb(self, template, values, expected):
        assert format_str(template, values) == expected

    def test_a_float_argument_keeps_its_shortest_decimal(self):
        """The boundary hands a cty number over as a Python float.

        `Decimal(0.1)` is the binary expansion, so formatting the float directly
        would print 0.1000000000000000055511151231257827.
        """
        assert format_str("%v", [0.1]) == "0.1"

    @pytest.mark.parametrize(
        ("template", "values", "message"),
        [
            # soup-go: {"ok":false,"error":"unsupported value for \"%d\" at 0:
            #           an integer is required"}
            ("%d items", [3.7], "an integer is required"),
            # soup-go: "not enough arguments for \"%s\" at 6: need index 1 but
            #           have 0 total"
            ("Hello %s", [], "not enough arguments"),
            # terraform console: format("%s", null) -> "null value cannot be formatted"
            ("%s", [None], "null value cannot be formatted"),
            # terraform console: format("100%") -> "invalid format string starting
            #                    at offset 4"
            ("100%", [], "invalid format string"),
        ],
    )
    def test_printf_refusal(self, template, values, message):
        with pytest.raises(FunctionError, match=message):
            format_str(template, values)

    def test_percent_v_renders_a_null_element_as_null(self):
        """terraform console: format("%v", null) -> "null"."""
        assert format_str("%v", [None]) == "null"


class TestFormatBracePlaceholders:
    """The components-only `{}` / `{0}` dialect, which `%` now takes precedence over.

    Braces are inert in Terraform's `format`, so supporting them is additive.
    A template containing a `%` is a printf template and its braces are literal,
    which is the rule that keeps the two dialects from colliding.
    """

    @pytest.mark.parametrize(
        ("template", "values", "expected"),
        [
            ("{} + {} = {}", [1, 2, 3], "1 + 2 = 3"),
            ("The value is {0}", [True], "The value is true"),
            ("{0} and {0}", ["a"], "a and a"),
        ],
    )
    def test_brace_placeholders_still_work(self, template, values, expected):
        assert format_str(template, values) == expected

    @pytest.mark.parametrize(
        ("template", "values"),
        [
            ('{"a": 1}', []),
            ('{"a": {"b": 2}}', []),
            ("{}", []),
        ],
    )
    def test_a_json_template_passes_through_untouched(self, template, values):
        """2026-08-17: `str.format()` read `{"a"` as a field name and raised
        `KeyError`, which reached the caller as a generic "execution failed" --
        every JSON template hit it. `terraform console` answers `"{}"` for
        `format("{}")`, so passing the template through also matches Terraform.
        """
        assert format_str(template, values) == template

    def test_a_json_template_with_a_placeholder_substitutes_only_the_placeholder(self):
        assert format_str('{"a": {}}', ["1"]) == '{"a": 1}'

    def test_too_many_values_is_refused(self):
        """2026-08-17: `format("{}", ["a", "b"])` answered `"a"` and dropped "b".

        terraform console: format("{}", "a", "b") -> "too many arguments; no
        verbs in format string". go-cty reports an argument the template never
        reaches rather than dropping it.
        """
        with pytest.raises(FunctionError, match="too many arguments"):
            format_str("{}", ["a", "b"])

    def test_a_template_with_no_placeholders_and_values_is_refused(self):
        with pytest.raises(FunctionError, match="no verbs in format string"):
            format_str("plain text", ["a"])

    def test_not_enough_values_is_refused(self):
        with pytest.raises(FunctionError, match="not enough arguments"):
            format_str("{} {}", ["a"])


class TestSplit:
    """Measured with `soup-go cty call split <sep> <string>`."""

    @pytest.mark.parametrize(
        ("delimiter", "string", "expected"),
        [
            # {"value":[""]} -- splitting a string always yields at least one part.
            # 2026-08-17: an `if not string: return []` short-circuit answered [].
            (",", "", [""]),
            # {"value":["a","b","c"]} -- 2026-08-17: `str.split("")` raised
            # `ValueError: empty separator`, which escaped as a bare Python
            # exception rather than anything a caller could act on.
            ("", "abc", ["a", "b", "c"]),
            # {"value":[]} -- Go's strings.Split("", "") yields nothing at all.
            ("", "", []),
            (",", "a,b,c", ["a", "b", "c"]),
            # soup-go cty call split '{"type":"string","value":""}'
            #   '{"type":"string","value":"héllo"}' -> ["h","é","l","l","o"]
            ("", "héllo", ["h", "é", "l", "l", "o"]),
        ],
    )
    def test_split(self, delimiter, string, expected):
        assert split(delimiter, string) == expected


class TestJoin:
    """Measured with `soup-go cty call join <sep> <list>` and `terraform console`."""

    def test_a_nested_collection_element_is_refused(self):
        """soup-go: join(", ", [["a"]]) -> {"ok":false,"error":"string required,
        but received list of string"}. terraform console reports it as "element 0:
        string required, but have tuple".

        2026-08-17: this answered `"['a']"` -- Python's repr of the inner list,
        square brackets and quotes and all, shipped to Terraform state.
        """
        with pytest.raises(FunctionError, match="element 0: string required, but have tuple"):
            join(", ", [["a"]])

    def test_a_map_element_is_refused(self):
        with pytest.raises(FunctionError, match="element 0: string required, but have object"):
            join(", ", [{"a": 1}])

    def test_a_null_element_is_refused(self):
        """terraform console: join(",", ["a", null]) -> "element 1 is null; cannot
        concatenate null values".

        2026-08-17: `str.join` raised a bare `TypeError` on the None here.
        """
        with pytest.raises(FunctionError, match="element 1 is null"):
            join(",", ["a", None])

    def test_numbers_and_booleans_still_join(self):
        """soup-go agrees with this one already, so it is pinned unchanged."""
        assert join(", ", [1, True]) == "1, true"


class TestReplaceTreatsSlashWrappedSearchAsRegex:
    """Terraform's `replace`, not go-cty's.

    `terraform console`, Terraform 1.14.0:

        replace("hello world", "/w.*d/", "x")           -> "hello x"
        replace("foo-bar", "/(\\w+)-(\\w+)/", "$2-$1")   -> "bar-foo"
        replace("hello", "//", "-")                     -> "-h-e-l-l-o-"
        replace("hello", "/", "-")                      -> "hello"
        replace("x", "/[/", "y")                        -> error parsing regexp
        replace("abc", "", "-")                         -> "-a-b-c-"

    2026-08-17: `search` was always taken literally, so the first two answered
    the subject unchanged.
    """

    @pytest.mark.parametrize(
        ("string", "search", "replacement", "expected"),
        [
            ("hello world", "/w.*d/", "x", "hello x"),
            ("foo-bar", r"/(\w+)-(\w+)/", "$2-$1", "bar-foo"),
            ("a1b2", "/[0-9]/", "#", "a#b#"),
            # A `/`-wrapped empty pattern matches between every character.
            ("hello", "//", "-", "-h-e-l-l-o-"),
            # One character is not a wrapper, so a lone "/" stays literal.
            ("a/b", "/", "-", "a-b"),
            ("hello", "/", "-", "hello"),
            # Already agreed before this change; pinned so it stays agreed.
            ("hello world", "world", "earth", "hello earth"),
            ("abc", "", "-", "-a-b-c-"),
            # A literal search is not a regex: "." matches only a dot.
            ("a.b", ".", "-", "a-b"),
        ],
    )
    def test_replace(self, string, search, replacement, expected):
        assert replace(string, search, replacement) == expected

    def test_an_invalid_pattern_is_refused(self):
        with pytest.raises(FunctionError, match="invalid regexp pattern"):
            replace("x", "/[/", "y")


class TestTostring:
    """Measured with `soup-go cty call tostring <arg-json>`."""

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            # {"value":"0.0000001"} -- 2026-08-17: `str(1e-7)` answered "1e-07",
            # Python's repr, which switches to scientific notation on its own.
            (1e-7, "0.0000001"),
            (-1e-7, "-0.0000001"),
            (1e20, "100000000000000000000"),
            # A cty number has no scale, so 3.0 and 3 are the same number.
            (3.0, "3"),
            # Already agreed; pinned so they stay agreed.
            (123, "123"),
            (123.45, "123.45"),
            (True, "true"),
            (False, "false"),
            ("hello", "hello"),
        ],
    )
    def test_tostring(self, value, expected):
        assert tostring(value) == expected

    @pytest.mark.parametrize(
        ("value", "kind"),
        [
            # {"ok":false,"error":"cannot convert tuple to string"}
            # 2026-08-17: answered "[1, 2]", Python's repr.
            ([1, 2], "tuple"),
            ((1, 2), "tuple"),
            # {"ok":false,"error":"cannot convert object to string"}
            # 2026-08-17: answered "{'a': 1}" -- note the Python repr's quotes.
            ({"a": 1}, "object"),
            ({1, 2}, "set"),
        ],
    )
    def test_a_collection_has_no_string_representation(self, value, kind):
        with pytest.raises(FunctionError, match=f"cannot convert {kind} to string"):
            tostring(value)


# 🧩🔧🔚
