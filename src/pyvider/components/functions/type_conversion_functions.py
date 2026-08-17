#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


"""Type conversion functions for data transformation."""

from decimal import Decimal, InvalidOperation
from typing import Any

from provide.foundation import logger

from pyvider.cty import CtyNumber, CtyString, convert
from pyvider.cty.exceptions import CtyError
from pyvider.exceptions import FunctionError
from pyvider.hub import register_function

# The go-cty type name for each native container the protocol boundary can hand
# us, so a refusal reads the way Terraform's own does.
#
# 2026-08-17: `tostring` used to answer `str(value)` for these, so
# `tostring([1, 2])` returned the Python repr `"[1, 2]"` and
# `tostring({"a": 1})` returned `"{'a': 1}"` -- single quotes and all -- and
# that repr shipped to Terraform state as if it were a conversion. Terraform
# refuses both: `cannot convert tuple to string` / `cannot convert object to
# string`.
_UNCONVERTIBLE_KINDS: tuple[tuple[type | tuple[type, ...], str], ...] = (
    ((list, tuple), "tuple"),
    ((set, frozenset), "set"),
    (dict, "object"),
)


def unconvertible_kind(value: Any) -> str | None:
    """go-cty's name for `value`'s type, if it has no string representation.

    Shared with `join`, which needs the same answer to report which element it
    refused and why.
    """
    for kinds, name in _UNCONVERTIBLE_KINDS:
        if isinstance(value, kinds):
            return name
    return None


def _number_to_string(value: Decimal | int | float) -> str:
    """A number as go-cty writes it: plain decimal, never scientific notation.

    2026-08-17: `str(value)` was used here, which is Python's repr and switches
    to scientific notation on its own -- `tostring(1e-7)` answered `"1e-07"`
    where Terraform answers `"0.0000001"`. Delegated to `pyvider.cty`'s verified
    number -> string conversion (go-cty's `big.Float.Text('f', -1)`) rather than
    re-deriving the rendering rules here.

    A float is routed through `Decimal(str(...))` first, because `Decimal(float)`
    takes the exact binary expansion and `123.45` would come back as
    `123.450000000000002842170943`.
    """
    exact = value if isinstance(value, Decimal) else Decimal(str(value))
    if not exact.is_finite():
        # No Terraform number is infinite or NaN, so there is no go-cty answer
        # to match; report the Python spelling rather than raise.
        return str(exact)
    return str(convert(CtyNumber().validate(exact), CtyString()).value)


@register_function(name="tostring", summary="Explicitly converts a value to a string.")
def tostring(value: Any | None) -> str | None:
    """Convert a value to its Terraform string representation.

    Booleans become `"true"`/`"false"`, numbers become plain decimal text, and
    strings pass through. A collection has no string representation in Terraform
    and is refused rather than rendered as a Python repr.
    """
    if value is None:
        return None
    if isinstance(value, bool):
        result = "true" if value else "false"
        logger.debug("Converted boolean to string", original_value=value, result=result)
        return result
    if isinstance(value, str):
        return value
    kind = unconvertible_kind(value)
    if kind is not None:
        raise FunctionError(f"cannot convert {kind} to string.", function_name="tostring")
    if isinstance(value, Decimal | int | float):
        try:
            return _number_to_string(value)
        except (CtyError, InvalidOperation, ValueError) as e:  # pragma: no cover - defensive
            raise FunctionError(f"cannot convert number to string: {e}", function_name="tostring") from e
    result = str(value)
    logger.debug(
        "Converted value to string",
        value_type=type(value).__name__,
        result_length=len(result),
    )
    return result


# 🔄🏷️🎯

# 🧩🔧🔚
