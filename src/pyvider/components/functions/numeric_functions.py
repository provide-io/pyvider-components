# pyvider/components/functions/numeric_functions.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# pyvider/components/functions/numeric_functions.py
#

from pyvider.exceptions import FunctionError
from pyvider.hub import register_function


@register_function(name="add", summary="Adds two numbers.")
def add(a: int | float | None, b: int | float | None) -> int | float | None:
    if a is None or b is None:
        return None
    try:
        result = a + b
        return (
            int(result) if isinstance(result, float) and result.is_integer() else result
        )
    except TypeError as e:
        raise FunctionError(f"Invalid argument types for addition: {e}") from e


@register_function(name="subtract", summary="Subtracts two numbers.")
def subtract(a: int | float | None, b: int | float | None) -> int | float | None:
    if a is None or b is None:
        return None
    try:
        result = a - b
        return (
            int(result) if isinstance(result, float) and result.is_integer() else result
        )
    except TypeError as e:
        raise FunctionError(f"Invalid argument types for subtraction: {e}") from e


@register_function(name="multiply", summary="Multiplies two numbers.")
def multiply(a: int | float | None, b: int | float | None) -> int | float | None:
    if a is None or b is None:
        return None
    try:
        result = a * b
        return (
            int(result) if isinstance(result, float) and result.is_integer() else result
        )
    except TypeError as e:
        raise FunctionError(f"Invalid argument types for multiplication: {e}") from e


@register_function(name="divide", summary="Divides two numbers.")
def divide(a: int | float | None, b: int | float | None) -> int | float | None:
    if a is None or b is None:
        return None
    if b == 0:
        raise FunctionError("Division by zero.")
    try:
        result = a / b
        return (
            int(result) if isinstance(result, float) and result.is_integer() else result
        )
    except TypeError as e:
        raise FunctionError(f"Invalid argument types for division: {e}") from e


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
def sum_list(numbers: list[int | float] | None) -> int | float | None:
    if numbers is None:
        return None
    result = sum(numbers)
    return int(result) if isinstance(result, float) and result.is_integer() else result


@register_function(
    name="round",
    summary="Rounds a number to a specified precision.",
    param_descriptions={
        "number": "The number to round",
        "options": "Optional: Precision (decimal places, default: 0)",
    },
)
def round_number(number: int | float | None, *options) -> int | float | None:
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
    """
    if number is None:
        return None

    # Extract precision from variadic args (default: 0)
    precision = int(options[0]) if options and len(options) > 0 else 0

    try:
        return round(number, precision)
    except TypeError as e:
        raise FunctionError(f"Invalid argument types for round: {e}") from e


# 🔢➕🎯
# 🧩🔧🔣🪄
