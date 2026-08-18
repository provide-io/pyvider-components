#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Terraform parity for the numeric and collection functions.

Every expectation in this file was measured on 2026-08-17 against real go-cty
with the differential harness (`soup-go cty call <function> <arg-json>...`), and
the command that produced it is quoted beside it. The two exceptions are `sum`
and `round`, which go-cty's stdlib does not have -- `soup-go cty functions` lists
neither -- and whose reference is named where they are tested.

The harness is not invoked from here on purpose: it lives outside this repo and
these functions are pure, so the measured answers are pinned as literals and the
sweep that produced them stays reproducible from the quoted commands.
"""

from decimal import Decimal

import pytest
from pyvider.exceptions import FunctionError

from pyvider.components.functions.collection_functions import contains, length
from pyvider.components.functions.numeric_functions import (
    add,
    divide,
    multiply,
    round_number,
    subtract,
    sum_list,
)

FAMILY = "\U0001f468\u200d\U0001f469\u200d\U0001f467\u200d\U0001f466"
"""MAN ZWJ WOMAN ZWJ GIRL ZWJ BOY: seven code points, one grapheme cluster."""

E_ACUTE = "e\u0301"
"""LATIN SMALL LETTER E followed by COMBINING ACUTE ACCENT, not the precomposed U+00E9."""

US_FLAG = "\U0001f1fa\U0001f1f8"
"""REGIONAL INDICATOR SYMBOL LETTER U and S: two code points, one cluster."""


class TestLengthCountsGraphemeClusters:
    """`length` of a string counts what a reader counts, not code points.

    Terraform's `length` hands the string case to go-cty's `strlen`. Measured:

        soup-go cty call strlen '{"type":"string","value":"<value>"}'

    which answered 1 for each of the three below and 5 for "hello", where
    Python's `len` answered 7, 2, 2 and 5.
    """

    @pytest.mark.parametrize(
        ("value", "code_points", "clusters"),
        [
            (FAMILY, 7, 1),
            (E_ACUTE, 2, 1),
            (US_FLAG, 2, 1),
            ("hello", 5, 5),
        ],
    )
    def test_string_length_is_grapheme_clusters(self, value, code_points, clusters):
        assert len(value) == code_points, "the fixture no longer holds the code points it claims"
        assert length(value) == clusters

    def test_ascii_length_is_unchanged(self):
        """Pinned by tests/test_tdd_stdlib_functions.py:29 and still true."""
        assert length("hello") == 5

    @pytest.mark.parametrize(
        ("collection", "expected"),
        [
            (["a", "b", "c"], 3),
            ({"a": 1, "b": 2}, 2),
            (("a", "b"), 2),
            ({"a", "b"}, 2),
            ([], 0),
            ({}, 0),
        ],
    )
    def test_collection_length_still_counts_elements(self, collection, expected):
        """Only the string branch changed; a collection is still measured in elements.

        A set and a map are included because the protocol boundary delivers them
        as `list` and `dict`, and go-cty agrees on the counts:
        `soup-go cty call length '{"type":["map","string"],"value":{"a":"1"}}'` -> 1.
        """
        assert length(collection) == expected

    def test_length_of_a_multi_cluster_string_sums_clusters(self):
        assert length(FAMILY + US_FLAG + "ab") == 4

    @pytest.mark.parametrize(("value", "named"), [(5, "number"), (3.5, "number"), (True, "bool")])
    def test_length_of_a_non_collection_is_an_actionable_error(self, value, named):
        """Was `TypeError: object of type 'int' has no len()`, a Python-internal message.

        go-cty's own refusals name the accepted types --
        `soup-go cty call length '{"type":"number","value":5}'` -> "collection must be
        a list, a map or a tuple", and `strlen` on the same argument -> "string
        required, but received number" -- so this one does too.
        """
        with pytest.raises(FunctionError) as raised:
            length(value)
        message = str(raised.value)
        assert "a list, a map, or a string is required" in message
        assert f"received {named}" in message

    def test_length_of_null_is_still_null(self):
        """The null->null policy is out of scope and stays."""
        assert length(None) is None


class TestContainsIsTypeAware:
    r"""`contains` no longer conflates a bool with a number.

    Python's `bool` subclasses `int`, so `element in list_to_check` answered
    `true` for both cases below. Measured:

        soup-go cty call contains '{"type":["list","number"],"value":[1,2,3]}' \
            '{"type":"bool","value":true}'
        -> {"ok":true,"type":"bool","value":false}
        soup-go cty call contains '{"type":["list","number"],"value":[0]}' \
            '{"type":"bool","value":false}'
        -> {"ok":true,"type":"bool","value":false}
    """

    def test_true_is_not_one(self):
        assert contains([1, 2, 3], True) is False

    def test_false_is_not_zero(self):
        assert contains([0], False) is False

    def test_one_is_not_true(self):
        """The mirror image: a number looked for in a list of bools."""
        assert contains([True, False], 1) is False

    def test_a_bool_still_matches_a_bool(self):
        assert contains([True], True) is True
        assert contains([False], False) is True
        assert contains([True], False) is False

    def test_a_number_still_matches_across_spellings(self):
        """`soup-go cty call contains '{"type":["list","number"],"value":[1]}'
        '{"type":"number","value":1.0}'` -> `true`: 1 and 1.0 are one number."""
        assert contains([1], 1.0) is True
        assert contains([1.0], 1) is True
        assert contains([Decimal("1")], 1) is True

    def test_a_number_still_does_not_match_a_string(self):
        assert contains(["1"], 1) is False

    @pytest.mark.parametrize(
        ("collection", "element", "expected"),
        [
            ([[1]], [True], False),
            ([[1]], [1], True),
            ([{"a": 1}], {"a": True}, False),
            ([{"a": 1}], {"a": 1}, True),
            ([{"a": 1}], {"b": 1}, False),
            ([[1, 2]], [1], False),
        ],
    )
    def test_the_distinction_holds_inside_nested_collections(self, collection, element, expected):
        """`soup-go cty call contains '{"type":["list",["list","number"]],"value":[[1]]}'
        '{"type":["list","bool"],"value":[true]}'` -> `false`."""
        assert contains(collection, element) is expected

    def test_plain_membership_is_unchanged(self):
        assert contains(["a", "b", "c"], "b") is True
        assert contains(["a", "b", "c"], "d") is False

    def test_contains_with_null_list_is_still_null(self):
        assert contains(None, "a") is None

    def test_contains_with_a_null_element_is_still_false(self):
        """The null policy, unchanged, and go-cty agrees here anyway:
        `soup-go cty call contains '{"type":["list","string"],"value":["a"]}'
        '{"type":"string","null":true}'` -> `false`."""
        assert contains(["a"], None) is False


class TestSumRefusesAnEmptyList:
    """`sum([])` returned `0`; Terraform refuses.

    go-cty's stdlib has no `sum` (`soup-go cty functions` does not list it), so
    the reference is Terraform's own `SumFunc` in
    `internal/lang/funcs/collection.go`, which answers
    "cannot sum an empty list" for a zero-length argument.
    """

    def test_empty_list_is_an_error(self):
        with pytest.raises(FunctionError, match="empty list"):
            sum_list([])

    def test_sum_of_integers_is_unchanged(self):
        assert sum_list([1, 2, 3]) == 6

    def test_sum_of_numeric_strings(self):
        """From Terraform this case never arises: `sum`'s parameter is declared
        `list(number)`, so the boundary has already converted `["1", "2"]` to
        numbers before the function sees it, and the answer agreed before this
        change. Called directly from Python the old implementation raised
        `TypeError: unsupported operand type(s) for +: 'int' and 'str'`; `Decimal`
        parses the digits instead, which is incidental rather than a fix, and
        pinned here so it is a known consequence rather than a surprise."""
        assert sum_list(["1", "2"]) == 3

    def test_sum_agrees_with_add_on_the_same_numbers(self):
        """`sum([0.1, 0.2])` and `add(0.1, 0.2)` both answered 0.30000000000000004
        before; both are 0.3 now, so the two no longer have to be reconciled."""
        assert sum_list([0.1, 0.2]) == Decimal("0.3")
        assert sum_list([0.1, 0.2]) == add(0.1, 0.2)

    def test_sum_of_null_is_still_null(self):
        assert sum_list(None) is None


class TestArithmeticIsExact:
    """The four operators compute to Terraform's precision, not float64's.

    Terraform's `+`, `-`, `*` and `/` are go-cty's `add`, `subtract`, `multiply`
    and `divide`, computed in a 512-bit `big.Float`. Each command below was run
    as `soup-go cty call <op> '{"type":"number","value":<a>}'
    '{"type":"number","value":<b>}'`.
    """

    def test_add_of_two_tenths(self):
        """Was 0.30000000000000004; harness answers 0.3."""
        assert add(0.1, 0.2) == Decimal("0.3")

    def test_subtract_of_tenths(self):
        """Was 0.19999999999999998; harness answers 0.2000...0002 (155 digits),
        whose leading digits are 0.2 -- a binary mantissa's artefact that a
        decimal one does not have."""
        assert subtract(0.3, 0.1) == Decimal("0.2")

    def test_multiply_of_tenths(self):
        """Was 1.2100000000000002; harness answers 1.2100...0001."""
        assert multiply(1.1, 1.1) == Decimal("1.21")

    def test_divide_carries_terraform_s_digit_count(self):
        """Was 0.3333333333333333 (16 digits). The harness answers 155
        significant digits, because 512 mantissa bits is 154.1 decimal digits."""
        quotient = divide(1, 3)
        assert isinstance(quotient, Decimal)
        assert len(str(quotient).split(".")[1]) == 155
        assert str(quotient).startswith("0.33333333333333333")

    def test_large_magnitudes_do_not_become_infinity(self):
        """Was `inf`, which marshalled as `Decimal("Infinity")`. The harness
        answers the exact integer 2 followed by 308 zeroes."""
        total = add(1e308, 1e308)
        assert total == int("2" + "0" * 308)

    def test_repeated_addition_does_not_drift(self):
        """Ten tenths were 0.9999999999999999; they are now 1."""
        total: object = 0
        for _ in range(10):
            total = add(total, 0.1)
        assert total == 1

    @pytest.mark.parametrize(
        ("result", "expected"),
        [
            (add(1, 2), 3),
            (add(1.5, 1.5), 3),
            (subtract(10, 4), 6),
            (multiply(3, 4), 12),
            (divide(1200, 4), 300),
        ],
    )
    def test_an_integral_result_is_still_an_int(self, result, expected):
        """`cty_to_native` hands an integral number in as an `int` and the
        boundary expects one back -- `tostring(1.0)` is `"1"` because of it."""
        assert result == expected
        assert isinstance(result, int)

    def test_a_non_integral_result_is_an_exact_decimal(self):
        assert divide(10, 4) == Decimal("2.5")
        assert isinstance(divide(10, 4), Decimal)

    @pytest.mark.parametrize(
        ("numerator", "denominator", "expected"),
        [
            (1, 0, Decimal("Infinity")),
            (-1, 0, Decimal("-Infinity")),
            (1.0, 0, Decimal("Infinity")),
            (-1.0, 0, Decimal("-Infinity")),
        ],
    )
    def test_division_by_zero_is_a_signed_infinity(self, numerator, denominator, expected):
        """This pinned "Division by zero." as an error on all three of `1/0`,
        `-1/0` and `0/0`, which was wrong: Terraform's own `/` and go-cty's
        `divide` agree with each other and disagree with that. Measured
        2026-08-17 with `terraform console` (OpenTofu): `1/0` -> `+Inf`, `-1/0`
        -> `-Inf`. See `_divide`."""
        assert divide(numerator, denominator) == expected

    def test_zero_divided_by_zero_is_undefined(self):
        """The one case a signed infinity cannot answer. Measured 2026-08-17
        with `terraform console` (OpenTofu): `0/0` -> "Error: can't divide zero
        by zero or infinity by infinity" -- the same wording go-cty's own
        `divide` raises, and pyvider-cty's `divide` matches it exactly."""
        with pytest.raises(FunctionError, match="can't divide zero by zero or infinity by infinity"):
            divide(0, 0)

    def test_negative_zero_divided_by_zero_is_also_undefined(self):
        """`-0.0` is still zero for this purpose, matching go-cty and `Decimal`."""
        with pytest.raises(FunctionError, match="can't divide zero by zero or infinity by infinity"):
            divide(-0.0, 0)

    @pytest.mark.parametrize("operation", [add, subtract, multiply, divide])
    def test_a_null_operand_is_still_null(self, operation):
        assert operation(1, None) is None
        assert operation(None, 1) is None

    @pytest.mark.parametrize("operation", [add, subtract, multiply, divide])
    def test_a_non_numeric_operand_is_an_actionable_error(self, operation):
        with pytest.raises(FunctionError, match="two numbers are required"):
            operation(object(), 1)


class TestRoundIsUnchanged:
    """`round` has no reference answer and was deliberately not changed.

    It is not a Terraform builtin and not in go-cty's stdlib: `soup-go cty
    functions` lists `ceil`, `floor` and `signum` and no `round`. These pin the
    current banker's rounding so that a change to it has to be a decision rather
    than an accident. See `round_number`'s docstring. 2026-08-17.
    """

    @pytest.mark.parametrize(("value", "expected"), [(2.5, 2), (0.5, 0), (-2.5, -2), (3.5, 4)])
    def test_ties_round_to_even(self, value, expected):
        assert round_number(value) == expected

    def test_precision_is_honoured(self):
        assert round_number(3.14159, 2) == 3.14

    def test_round_of_null_is_still_null(self):
        assert round_number(None) is None


@pytest.mark.usefixtures("discovered_components_session")
class TestThroughTheProtocolBoundary:
    """The answers survive the trip Terraform actually makes.

    A `Decimal` with 155 digits is only a fix if it reaches the wire, so these
    drive the same handler Terraform's gRPC call reaches.
    """

    @staticmethod
    async def _call(name: str, *args: tuple[object, object]) -> object:
        """Dispatch `name` through the real handler.

        Each argument is paired with the cty type the function's published
        schema declares for that position, because that is the type the handler
        decodes it with; handing everything over as `dynamic` would be testing a
        call Terraform never makes.
        """
        import pyvider.protocols.tfprotov6.protobuf as pb
        from pyvider.conversion import marshal, unmarshal
        from pyvider.functions.adapters import function_to_dict
        from pyvider.hub import hub
        from pyvider.protocols.tfprotov6.handlers import CallFunctionHandler

        request = pb.CallFunction.Request(
            name=name,
            arguments=[marshal(value, schema=schema) for value, schema in args],
        )
        response = await CallFunctionHandler(request, context=None)
        assert not response.error.text, response.error.text
        return_type = function_to_dict(hub.get_component("function", name))["return"]["cty_type"]
        return unmarshal(response.result, schema=return_type).value

    async def test_length_of_an_emoji_is_one_over_the_wire(self):
        from pyvider.cty import CtyDynamic

        assert await self._call("length", (FAMILY, CtyDynamic())) == 1

    async def test_add_of_two_tenths_is_three_tenths_over_the_wire(self):
        from pyvider.cty import CtyNumber

        assert await self._call("add", (0.1, CtyNumber()), (0.2, CtyNumber())) == Decimal("0.3")

    async def test_divide_keeps_its_digits_over_the_wire(self):
        from pyvider.cty import CtyNumber

        quotient = await self._call("divide", (1, CtyNumber()), (3, CtyNumber()))
        assert len(str(quotient).split(".")[1]) == 155

    async def test_divide_by_zero_is_still_infinity_over_the_wire(self):
        """The function returns native `Decimal("Infinity")`; this confirms it
        survives marshalling rather than becoming `null`, an error, or a
        finite number by the time it reaches the wire."""
        from pyvider.cty import CtyNumber

        quotient = await self._call("divide", (1, CtyNumber()), (0, CtyNumber()))
        assert quotient == Decimal("Infinity")

        quotient = await self._call("divide", (-1, CtyNumber()), (0, CtyNumber()))
        assert quotient == Decimal("-Infinity")

    async def test_a_large_sum_is_not_infinity_over_the_wire(self):
        """The operand is spelled as a `Decimal` because that is what the wire carries.

        go-cty's msgpack encoder writes a number as a float64 only when the
        float64 is exact, and 10^308 is not a binary float, so Terraform sends
        the decimal digits and the provider receives 10^308 rather than the
        nearest float. Marshalling a Python `float` here instead would test an
        argument Terraform never sends -- the binary neighbour of 10^308 --
        and the answer would be twice *that*.
        """
        from pyvider.cty import CtyNumber

        total = await self._call("add", (Decimal("1e308"), CtyNumber()), (Decimal("1e308"), CtyNumber()))
        assert total == int("2" + "0" * 308)

    async def test_contains_does_not_conflate_true_with_one_over_the_wire(self):
        from pyvider.cty import CtyBool, CtyDynamic, CtyList

        found = await self._call(
            "contains",
            ([1, 2, 3], CtyList(element_type=CtyDynamic())),
            (True, CtyBool()),
        )
        assert found is False


# 🧩🔧🔚
