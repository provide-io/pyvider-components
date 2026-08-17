#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


"""Numeric computation functions for mathematical operations."""

import operator
from collections.abc import Callable
from decimal import Decimal, localcontext
from typing import Any

from pyvider.exceptions import FunctionError
from pyvider.hub import register_function

_GO_CTY_PRECISION = 155
"""Significant decimal digits, chosen to be the count Terraform's answers carry.

Terraform holds every number in a `big.Float` with a 512-bit mantissa, and 512
bits is 154.1 decimal digits, so go-cty's answers run to 155 significant
digits. Measured 2026-08-17:

    soup-go cty call divide '{"type":"number","value":1}' '{"type":"number","value":3}'
    -> 0.33333333...335   (155 significant digits)

A `decimal` context of 155 digits therefore answers with as many digits as
Terraform does. It cannot be bit-identical -- go-cty's mantissa is binary, which
is where the trailing `...335` and the `0.2000...0002` of `subtract(0.3, 0.1)`
come from, and a decimal mantissa has no such artefact -- so where the two
differ, this one is the more exact of the two.
"""


def _as_decimal(value: Any) -> Decimal:
    """The number the caller wrote, as an exact `Decimal`.

    A `float` goes through `str` deliberately. `Decimal(0.1)` is the *binary*
    float, 0.1000000000000000055511151231257827021181583404541015625, and adding
    two of those is precisely how `add(0.1, 0.2)` came to answer
    0.30000000000000004. `Decimal(str(0.1))` is `Decimal("0.1")`, because
    `repr` of a float is the shortest decimal that round-trips to it -- which is
    the literal the practitioner wrote in their configuration and the literal
    Terraform parsed into its own number. Going through `str` is what makes
    `add(0.1, 0.2)` answer 0.3.

    Everything else goes to `Decimal` directly: an `int` (including a `bool`) is
    already exact, and a `Decimal` is returned untouched.
    """
    if isinstance(value, float):
        return Decimal(str(value))
    return Decimal(value)


def _as_number(result: Decimal) -> int | Decimal:
    """An integral result as an `int`, anything else as an exact `Decimal`.

    The boundary hands an integral number *in* as an `int` -- which is why
    `tostring(1.0)` is `"1"` -- so an integral answer goes back the same way,
    preserving the shape the `float` implementation returned while keeping every
    non-integral digit that implementation lost.
    """
    if result.is_finite() and result == result.to_integral_value():
        return int(result)
    return result


def _arithmetic(
    operation: Callable[[Decimal, Decimal], Decimal],
    a: Any,
    b: Any,
    what: str,
) -> int | Decimal:
    """One arithmetic operation, computed to Terraform's precision.

    Terraform's `+`, `-`, `*` and `/` are go-cty's `add`, `subtract`, `multiply`
    and `divide`, which compute in a 512-bit `big.Float`. These functions
    computed in `float`, so measured 2026-08-17 (`soup-go cty call ...`) they
    answered:

        add(0.1, 0.2)      was 0.30000000000000004, Terraform 0.3
        subtract(0.3, 0.1) was 0.19999999999999998, Terraform 0.2000...0002
        multiply(1.1, 1.1) was 1.2100000000000002,  Terraform 1.2100...0001
        divide(1, 3)       was 16 digits,           Terraform 155 digits
        add(1e308, 1e308)  was inf,                 Terraform 2 with 308 zeroes

    `decimal` is the stdlib's arbitrary-precision arithmetic, so no new
    dependency is involved; see `_GO_CTY_PRECISION` for the digit count and
    `_as_decimal` for why the operands are spelled the way they are.
    """
    try:
        with localcontext() as context:
            context.prec = _GO_CTY_PRECISION
            return _as_number(operation(_as_decimal(a), _as_decimal(b)))
    except (ArithmeticError, TypeError, ValueError) as e:
        raise FunctionError(
            f"Invalid argument types for {what}: two numbers are required, "
            f"but received {type(a).__name__} and {type(b).__name__}."
        ) from e


@register_function(name="add", summary="Adds two numbers.")
def add(a: int | float | Decimal | None, b: int | float | Decimal | None) -> int | Decimal | None:
    """Add two numbers exactly; see `_arithmetic`. 2026-08-17."""
    if a is None or b is None:
        return None
    return _arithmetic(operator.add, a, b, "addition")


@register_function(name="subtract", summary="Subtracts two numbers.")
def subtract(a: int | float | Decimal | None, b: int | float | Decimal | None) -> int | Decimal | None:
    """Subtract two numbers exactly; see `_arithmetic`. 2026-08-17."""
    if a is None or b is None:
        return None
    return _arithmetic(operator.sub, a, b, "subtraction")


@register_function(name="multiply", summary="Multiplies two numbers.")
def multiply(a: int | float | Decimal | None, b: int | float | Decimal | None) -> int | Decimal | None:
    """Multiply two numbers exactly; see `_arithmetic`. 2026-08-17."""
    if a is None or b is None:
        return None
    return _arithmetic(operator.mul, a, b, "multiplication")


@register_function(name="divide", summary="Divides two numbers.")
def divide(a: int | float | Decimal | None, b: int | float | Decimal | None) -> int | Decimal | None:
    """Divide two numbers to Terraform's precision; see `_arithmetic`. 2026-08-17.

    The refusal to divide by zero is unchanged and deliberate. It is *not*
    go-cty's behaviour: measured 2026-08-17,
    `soup-go cty call divide '{"type":"number","value":1}' '{"type":"number","value":0}'`
    answers `ok:true` with `+Inf`. Changing that is a separate decision from
    fixing the arithmetic, so it is left as it stands.
    """
    if a is None or b is None:
        return None
    if b == 0:
        raise FunctionError("Division by zero.")
    return _arithmetic(operator.truediv, a, b, "division")


@register_function(name="min", summary="Finds the minimum value in a list of numbers.")
def min_value(numbers: list[int | float] | None) -> int | float | None:
    if numbers is None:
        return None
    if not numbers:
        raise FunctionError("min() requires at least one number.")
    return min(numbers)


@register_function(name="max", summary="Finds the maximum value in a list of numbers.")
def max_value(numbers: list[int | float] | None) -> int | float | None:
    if numbers is None:
        return None
    if not numbers:
        raise FunctionError("max() requires at least one number.")
    return max(numbers)


@register_function(name="sum", summary="Calculates the sum of a list of numbers.")
def sum_list(numbers: list[int | float | Decimal] | None) -> int | Decimal | None:
    """Total a list of numbers, refusing an empty list.

    This returned `0` for `[]`. Terraform's `sum` refuses -- "cannot sum an
    empty list" (`internal/lang/funcs/collection.go`) -- because there is no
    number the sum of nothing could be, and `0` turns a mistake into a plan
    instead of an error. The differential harness cannot settle this one:
    `soup-go cty functions` does not list `sum`, because `sum` is Terraform's
    own function rather than one of go-cty's stdlib, so the reference here is
    Terraform's implementation and its documentation. 2026-08-17.

    Terraform accumulates with the same `Add` the `+` operator uses, so the
    total is accumulated in `Decimal` for the reason given in `_arithmetic`:
    `sum([0.1, 0.2])` was 0.30000000000000004 and is now 0.3, which is also what
    `add(0.1, 0.2)` answers -- previously the two disagreed.
    """
    if numbers is None:
        return None
    if not numbers:
        raise FunctionError("Cannot sum an empty list.")
    total: int | Decimal = 0
    for number in numbers:
        total = _arithmetic(operator.add, total, number, "summation")
    return total


@register_function(
    name="round",
    summary="Rounds a number to a specified precision.",
    param_descriptions={
        "number": "The number to round",
        "options": "Optional: Precision (decimal places, default: 0)",
    },
)
def round_number(number: int | float | None, *options: int) -> int | float | None:
    """
    Round a number to specified decimal places.

    Args:
        number: Number to round
        *options: Optional precision (int, default: 0)

    Returns:
        Rounded number

    Examples:
        round_number(3.14159) → 3
        round_number(3.14159, 2) → 3.14

    Note:
        `round` is not a Terraform builtin and is not in go-cty's stdlib
        (`soup-go cty functions` lists `ceil`, `floor` and `signum`, not
        `round`), so there is no reference answer to match and the behaviour
        below is this provider's own. It is Python's `round`, which rounds a
        tie to the nearest *even* result: `round(2.5)` is 2, `round(0.5)` is 0
        and `round(-2.5)` is -2, where a practitioner writing `round(2.5)`
        most likely expects 3. Left as it stands and documented rather than
        changed quietly, because changing it is a behaviour change for existing
        callers and belongs to whoever owns that decision. 2026-08-17.
    """
    if number is None:
        return None

    # Extract precision from variadic args (default: 0)
    precision = int(options[0]) if options and len(options) > 0 else 0

    try:
        return round(number, precision)
    except TypeError as e:
        raise FunctionError(f"Invalid argument types for round: {e}") from e


# 🔢+🎯

# 🧩🔧🔚
