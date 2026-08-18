#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


"""String manipulation functions for text processing.

The names here that collide with a Terraform builtin -- `upper`, `lower`,
`format`, `join`, `split`, `replace` -- answer what Terraform answers, because a
practitioner writing `provider::pyvider::upper(x)` reasonably expects the builtin
of that name. Divergences found by differential testing against real go-cty and
`terraform console` on 2026-08-17 are recorded at the function that fixed them.
"""

import re
from decimal import Decimal
from itertools import count
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient
from provide.foundation.formatting import (
    format_size,
    pluralize,
    to_camel_case,
    to_kebab_case,
    to_snake_case,
    truncate,
)

from pyvider.cty import CtyDynamic, CtyString, CtyValue
from pyvider.cty.conversion import infer_cty_type_from_raw
from pyvider.cty.exceptions import CtyError
from pyvider.cty.functions.format_functions import format_fn as _cty_format
from pyvider.cty.functions.string_functions import regexreplace as _cty_regexreplace
from pyvider.exceptions import FunctionError
from pyvider.hub import register_function

from .type_conversion_functions import tostring, unconvertible_kind

# `{}` and `{0}`: the Python-style positional placeholders this function has
# always accepted. Deliberately narrower than `str.format()`'s field syntax --
# see `format_str`.
_POSITIONAL_BRACE = re.compile(r"\{(\d*)\}")


def _simple_upper_char(char: str) -> str:
    """One code point's simple uppercase, the mapping Go's `strings.ToUpper` uses.

    Go maps case one rune at a time through `UnicodeData.txt`'s simple mapping
    and ignores `SpecialCasing.txt` entirely. Python applies the full mapping,
    which can lengthen a string. Where the full mapping produces more than one
    code point, the simple mapping is either the code point itself (`ß` stays
    `ß`, `ﬁ` stays `ﬁ`) or the titlecase code point (the 27 Greek letters with
    ypogegrammeni, whose simple uppercase is a single prosgegrammeni form).

    Derived rather than tabulated: checked at all 1,114,112 code points against
    `pyvider.cty._unicode.case.simple_upper`, which is generated from Go's own
    tables, and it agrees at every one. That module is explicitly private
    (`pyvider/cty/_unicode/__init__.py`: "Nothing here is part of the public
    API"), so importing it across the package boundary would couple this
    function to a name `pyvider-cty` does not promise to keep, and a released
    `pyvider-cty>=0.5.0` without it would fail this whole module's import. When
    a public alias lands -- alongside `pyvider.cty.graphemes` -- prefer it over
    both this and a second copy of the table.
    """
    mapped = char.upper()
    if len(mapped) == 1:
        return mapped
    titled = char.title()
    return titled if len(titled) == 1 else char


def _simple_lower_char(char: str) -> str:
    """One code point's simple lowercase, the mapping Go's `strings.ToLower` uses.

    Only U+0130 lengthens under Python's full mapping, and its simple lowercase
    is the first code point of that expansion, a bare `i`. Iterating one code
    point at a time also takes the final-sigma rule out of play, since that rule
    needs the neighbours to fire. Checked at all 1,114,112 code points against
    `pyvider.cty._unicode.case.simple_lower`; see `_simple_upper_char` for why
    that module is not imported.
    """
    mapped = char.lower()
    return mapped if len(mapped) == 1 else mapped[0]


@register_function(name="upper", summary="Converts a string to uppercase.")
def upper(input_str: str | None) -> str | None:
    """
    Convert a string to uppercase.

    2026-08-17: this was `input_str.upper()`, Python's *full* case mapping, where
    Terraform's `upper` is Go's `strings.ToUpper` and maps one code point at a
    time. Measured: `upper("straße")` answered `"STRASSE"` and `upper("ﬁ")`
    answered `"FI"`; Terraform answers `"STRAßE"` and `"ﬁ"`.

    Args:
        input_str: String to convert

    Returns:
        Uppercase string

    Examples:
        upper("hello") → "HELLO"
        upper("straße") → "STRAßE"
    """
    if input_str is None:
        return None
    return "".join(_simple_upper_char(char) for char in input_str)


@register_function(name="lower", summary="Converts a string to lowercase.")
def lower(input_str: str | None) -> str | None:
    """
    Convert a string to lowercase.

    2026-08-17: this was `input_str.lower()`, which applies both the full case
    mapping and the context-sensitive final-sigma rule that Go does not
    implement. Measured: `lower` of two GREEK CAPITAL LETTER SIGMA answered
    U+03C3 U+03C2 -- a final sigma -- where Terraform answers U+03C3 twice, and
    `lower` of U+0130 answered two code points where Terraform answers a bare
    `i`.

    Args:
        input_str: String to convert

    Returns:
        Lowercase string

    Examples:
        lower("HELLO") → "hello"
    """
    if input_str is None:
        return None
    return "".join(_simple_lower_char(char) for char in input_str)


def _exact(value: Any) -> Any:
    """`value` with every float replaced by its shortest exact decimal.

    The protocol boundary hands a cty number over as a Python float, and
    `Decimal(float)` takes the binary expansion -- 123.45 would reach the
    formatter as 123.450000000000002842170943 and print that way.
    """
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, list | tuple):
        return [_exact(item) for item in value]
    if isinstance(value, dict):
        return {key: _exact(item) for key, item in value.items()}
    return value


def _as_cty(value: Any) -> CtyValue[Any]:
    """A native argument as the `CtyValue` the `pyvider.cty` helpers take."""
    exact = _exact(value)
    if exact is None:
        return CtyValue.null(CtyDynamic())
    inferred: CtyValue[Any] = infer_cty_type_from_raw(exact).validate(exact)
    return inferred


def _format_printf(template: str, values: list[Any]) -> str:
    """Terraform's `format`, delegated to `pyvider.cty`'s verified printf.

    Reused rather than re-derived: `pyvider.cty.functions.format_functions` is a
    port of go-cty's `format.go` checked against go-cty itself, including the
    parts that are easy to get subtly wrong -- `%v`'s JSON fallback, `%q`'s
    `strconv.Quote`, Go's two-digit exponents, and width and precision counted
    in grapheme clusters rather than code points.
    """
    try:
        result = _cty_format(_as_cty(template), *[_as_cty(value) for value in values])
    except CtyError as e:
        raise FunctionError(str(e).removeprefix("format: "), function_name="format") from e
    return str(result.value)


def _format_braces(template: str, values: list[Any]) -> str:
    """The `{}` / `{0}` placeholders this function has always accepted.

    Substituted here rather than by `str.format()`, so that every brace that is
    not a bare positional placeholder stays literal. `str.format()` reads
    `{"a": 1}` as a field named `"a"` and raised `KeyError`, which reached the
    caller as a generic "execution failed" -- every JSON template hit it.

    With no values at all there is nothing to substitute, and the template comes
    back untouched -- which is also what Terraform answers for `format("{}")`.
    """
    if not values:
        return template
    automatic = count()
    used: set[int] = set()

    def substitute(match: re.Match[str]) -> str:
        digits = match.group(1)
        index = int(digits) if digits else next(automatic)
        if index >= len(values):
            raise FunctionError(
                f"not enough arguments for placeholder {match.group(0)}: "
                f"need index {index + 1} but have {len(values)} total.",
                function_name="format",
            )
        used.add(index)
        rendered: str | None = tostring(values[index])
        if rendered is None:
            raise FunctionError(
                f"unsupported value for {match.group(0)}: null value cannot be formatted.",
                function_name="format",
                argument_index=index,
            )
        return rendered

    result = _POSITIONAL_BRACE.sub(substitute, template)
    highest = max(used) + 1 if used else 0
    if highest < len(values):
        # go-cty reports an unreached argument as an error rather than dropping
        # it, on the grounds that the caller believes it is being printed.
        # 2026-08-17: `format("{}", ["a", "b"])` used to answer `"a"`.
        detail = "no verbs in format string" if highest == 0 else f"only {highest} used by format string"
        raise FunctionError(f"too many arguments; {detail}.", function_name="format")
    return result


@register_function(name="format", summary="Formats a string using printf verbs or positional braces.")
@resilient()
def format_str(template: str | None, values: list[Any] | None) -> str | None:
    """
    Format a string template with positional arguments.

    Two dialects, and the template chooses between them:

    * If the template contains a `%`, it is a **printf** template and is
      formatted exactly as Terraform's `format` formats it -- `%s`, `%d`, `%f`,
      `%v`, `%t`, `%q`, `%x`, `%b`, `%o`, `%e`, `%g`, with flags, width,
      precision, argument indexes (`%[1]s`) and `%%` for a literal percent.
      Braces are inert, as they are in Terraform.
    * Otherwise the components-only `{}` / `{0}` placeholders apply. Every other
      brace is literal, so a JSON template passes through untouched.

    2026-08-17: the dispatch used to be `re.search(r"%[sdfrg]", template)`, which
    matches only a *bare* verb. Every verb carrying a flag, a width or a
    precision missed it, fell through to `str.format()`, and came back as literal
    text with no error at all -- `format("%.2f", [3.14159])` answered `"%.2f"`
    where Terraform answers `"3.14"`, and the format string shipped to state.
    `%x`, `%q`, `%v`, `%t`, `%b`, `%o`, `%e`, `%[1]s` and `%%` were all emitted
    literally for the same reason.

    Args:
        template: printf template, or a template with {} placeholders
        values: List of values to insert into template

    Returns:
        Formatted string

    Examples:
        format("Hello, %s!", ["World"]) → "Hello, World!"
        format("%.2f", [3.14159]) → "3.14"
        format("{} + {} = {}", [1, 2, 3]) → "1 + 2 = 3"
    """
    if template is None:
        return None
    value_list = list(values or [])
    result = _format_printf(template, value_list) if "%" in template else _format_braces(template, value_list)
    logger.debug("Formatted string", template=template, value_count=len(value_list))
    return result


@register_function(name="join", summary="Joins list elements with a delimiter.")
def join(delimiter: str | None, strings: list[Any] | None) -> str | None:
    """
    Join a list of strings with a delimiter.

    2026-08-17: elements were stringified with `tostring`, which was `str()` and
    so rendered a nested collection as a Python repr -- `join(", ", [["a"]])`
    answered `"['a']"`. Terraform refuses it: "element 0: string required, but
    have tuple". A null element used to escape as a bare `TypeError` from
    `str.join`; Terraform says "element N is null; cannot concatenate null
    values". Numbers and booleans already agreed and are unchanged.

    Args:
        delimiter: String to use as separator (default: "")
        strings: List of values to join

    Returns:
        Joined string

    Examples:
        join(", ", ["apple", "banana", "cherry"]) → "apple, banana, cherry"
        join("", ["a", "b", "c"]) → "abc"
    """
    if strings is None:
        return None
    delimiter_str = delimiter or ""
    parts: list[str] = []
    for index, element in enumerate(strings):
        if element is None:
            raise FunctionError(
                f"element {index} is null; cannot concatenate null values.",
                function_name="join",
                argument_index=index,
            )
        kind = unconvertible_kind(element)
        if kind is not None:
            raise FunctionError(
                f"element {index}: string required, but have {kind}.",
                function_name="join",
                argument_index=index,
            )
        parts.append(tostring(element) or "")
    return delimiter_str.join(parts)


@register_function(name="split", summary="Splits a string by a delimiter.")
def split(delimiter: str | None, string: str | None) -> list[str] | None:
    """
    Split a string by a delimiter.

    2026-08-17: an empty subject short-circuited to `[]`, so `split(",", "")`
    answered `[]` where Terraform answers `[""]` -- splitting a string always
    yields at least one part. An empty delimiter reached `str.split("")`, which
    raises `ValueError: empty separator`, and that escaped as a bare Python
    exception; Terraform answers `["a", "b", "c"]` for `split("", "abc")` and
    `[]` for `split("", "")`.

    Args:
        delimiter: Delimiter to split on (default: "")
        string: String to split

    Returns:
        List of string parts

    Examples:
        split(",", "a,b,c") → ["a", "b", "c"]
        split("", "abc") → ["a", "b", "c"]
        split(",", "") → [""]
    """
    if string is None:
        return None
    delimiter_str = delimiter or ""
    if not delimiter_str:
        # Go's `strings.Split(s, "")` splits after every UTF-8 rune, which is
        # one code point each -- and yields nothing at all for an empty string.
        return list(string)
    return string.split(delimiter_str)


def _regex_replace(subject: str, pattern: str, replacement: str) -> str:
    """`re.ReplaceAllString`, delegated to `pyvider.cty`'s `regexreplace`.

    Reused rather than re-derived so the Go replacement-template dialect --
    `$1`, `${name}`, `$$`, and a reference to a group that did not participate
    expanding to nothing -- has one implementation, the one checked against
    go-cty.
    """
    try:
        result = _cty_regexreplace(
            CtyString().validate(subject),
            CtyString().validate(pattern),
            CtyString().validate(replacement),
        )
    except CtyError as e:
        raise FunctionError(str(e).removeprefix("regexreplace: "), function_name="replace") from e
    return str(result.value)


@register_function(name="replace", summary="Replaces occurrences of a substring or regex match.")
def replace(string: str | None, search: str | None, replacement: str | None) -> str | None:
    """
    Replace all occurrences of a substring, or of a regex match.

    2026-08-17: `search` was always taken literally, so a pattern wrapped in
    forward slashes matched nothing -- `replace("hello world", "/w.*d/", "x")`
    answered `"hello world"` where Terraform answers `"hello x"`. Terraform's
    `replace` (its own, not go-cty's `stdlib.Replace`) treats a `search` of more
    than one character that both starts and ends with `/` as a regular
    expression, and lets the replacement refer to capture groups as `$1` or
    `${name}`.

    Args:
        string: String to modify
        search: Substring to find, or `/pattern/` for a regular expression
        replacement: String to replace with

    Returns:
        Modified string

    Examples:
        replace("hello world", "world", "earth") → "hello earth"
        replace("hello world", "/w.*d/", "x") → "hello x"
        replace("foo-bar", "/(\\w+)-(\\w+)/", "$2-$1") → "bar-foo"
    """
    if string is None:
        return None
    search_str = search or ""
    replacement_str = replacement or ""
    if len(search_str) > 1 and search_str.startswith("/") and search_str.endswith("/"):
        return _regex_replace(string, search_str[1:-1], replacement_str)
    return string.replace(search_str, replacement_str)


@register_function(name="to_snake_case", summary="Converts text to snake_case.")
def snake_case(text: str | None) -> str | None:
    """Convert text to snake_case using provide-foundation utilities."""
    if text is None:
        return None
    return to_snake_case(text)


@register_function(
    name="to_camel_case",
    summary="Converts text to camelCase or PascalCase.",
    param_descriptions={
        "text": "The text to convert",
        "options": "Optional: Pass true for PascalCase (default: false for camelCase)",
    },
)
def camel_case(text: str | None, *options: bool) -> str | None:
    """
    Convert text to camelCase (or PascalCase if upper_first is true).

    Args:
        text: Text to convert
        *options: Optional boolean for upper_first (default: False)

    Returns:
        Converted text in camelCase (default) or PascalCase

    Examples:
        camel_case("my_var") → "myVar"
        camel_case("my_var", True) → "MyVar"
    """
    if text is None:
        return None

    # Extract upper_first from variadic args (default: False)
    upper_first = bool(options[0]) if options and len(options) > 0 else False

    return to_camel_case(text, upper_first=upper_first)


@register_function(name="to_kebab_case", summary="Converts text to kebab-case.")
def kebab_case(text: str | None) -> str | None:
    """Convert text to kebab-case using provide-foundation utilities."""
    if text is None:
        return None
    return to_kebab_case(text)


@register_function(
    name="format_size",
    summary="Formats bytes as human-readable size.",
    param_descriptions={
        "size_bytes": "Size in bytes to format",
        "options": "Optional: Precision for decimal places (default: 1)",
    },
)
def format_file_size(size_bytes: int | None, *options: int) -> str | None:
    """
    Format bytes as human-readable size (e.g., "1.5 KB", "2.3 MB").

    Args:
        size_bytes: Size in bytes
        *options: Optional integer for precision (default: 1)

    Returns:
        Formatted size string

    Examples:
        format_file_size(1024) → "1.0 KB"
        format_file_size(1024, 2) → "1.00 KB"
    """
    if size_bytes is None:
        return None

    # Extract precision from variadic args (default: 1)
    precision = int(options[0]) if options and len(options) > 0 else 1

    return format_size(size_bytes, precision)


@register_function(
    name="truncate",
    summary="Truncates text to specified length.",
    param_descriptions={
        "text": "Text to truncate",
        "options": "Optional: First arg is max_length (default: 100), second is suffix (default: '...')",
    },
)
def truncate_text(text: str | None, *options: int | str) -> str | None:
    """
    Truncate text to specified length with optional suffix.

    Args:
        text: Text to truncate
        *options: Optional args:
            - First: max_length (int, default: 100)
            - Second: suffix (str, default: "...")

    Returns:
        Truncated text with suffix if needed

    Examples:
        truncate_text("Hello World") → "Hello World"
        truncate_text("Very long text...", 10) → "Very lo..."
        truncate_text("Very long text...", 10, ">>") → "Very long>>"
    """
    if text is None:
        return None

    # Extract max_length and suffix from variadic args
    max_length = 100
    suffix = "..."

    if options and len(options) > 0:
        max_length = int(options[0])
    if options and len(options) > 1:
        suffix = str(options[1])

    return truncate(text, max_length, suffix)


@register_function(
    name="pluralize",
    summary="Pluralizes a word based on count.",
    param_descriptions={
        "word": "Word to pluralize",
        "options": "Optional: First arg is count (default: 1), second is custom plural form",
    },
)
def pluralize_word(word: str | None, *options: int | str) -> str | None:
    """
    Pluralize a word based on count with optional custom plural form.

    Args:
        word: Word to pluralize
        *options: Optional args:
            - First: count (int, default: 1)
            - Second: plural (str, default: None for auto-pluralization)

    Returns:
        Singular or plural form based on count

    Examples:
        pluralize_word("apple") → "apple"
        pluralize_word("apple", 1) → "apple"
        pluralize_word("apple", 2) → "apples"
        pluralize_word("person", 2, "people") → "people"
    """
    if word is None:
        return None

    # Extract count and plural from variadic args
    count = 1
    plural = None

    if options and len(options) > 0:
        count = int(options[0])
    if options and len(options) > 1:
        plural = str(options[1]) if options[1] is not None else None

    return pluralize(count, word, plural)


# ✂️📝🎯

# 🧩🔧🔚
