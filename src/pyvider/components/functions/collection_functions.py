#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


"""Collection manipulation functions for arrays and objects."""

from decimal import Decimal
from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient

# Reuse, not reimplementation: `pyvider-cty` vendors the UAX#29 segmentation
# algorithm and verifies it against go-cty, so counting grapheme clusters here
# means importing that rather than growing a second Unicode table.
from pyvider.cty import grapheme_cluster_count
from pyvider.exceptions import FunctionError
from pyvider.hub import register_function

_COLLECTION_TYPES = (list, tuple, set, frozenset, dict)
"""What `length` will measure in elements: every shape a cty collection arrives as.

The protocol boundary hands a list or set over as a `list`, a tuple as a
`tuple`, and a map or object as a `dict`.
"""

_CTY_TYPE_NAMES = {bool: "bool", int: "number", float: "number", Decimal: "number", str: "string"}
"""Python types spelled the way an error message should name them.

A practitioner writing HCL knows `number`, not `int`, so an error that says
"received int" is describing an implementation they cannot see.
"""


def _cty_type_name(value: Any) -> str:
    """What Terraform would call this value's type."""
    return _CTY_TYPE_NAMES.get(type(value), type(value).__name__)


def _values_equal(left: Any, right: Any) -> bool:
    r"""Equality that keeps `true` apart from `1`.

    Python's `bool` is a subclass of `int`, so `1 == True` and `0 == False`, and
    `element in list_to_check` inherited that: `contains([1, 2, 3], true)`
    answered `true` and `contains([0], false)` answered `true`. Terraform
    answers `false` to both, because a bool and a number are different cty types
    and no value of one is ever equal to a value of the other. Measured
    2026-08-17:

        soup-go cty call contains '{"type":["list","number"],"value":[1,2,3]}' \
            '{"type":"bool","value":true}'
        -> {"ok":true,"type":"bool","value":false}
        soup-go cty call contains '{"type":["list",["list","number"]],"value":[[1]]}' \
            '{"type":["list","bool"],"value":[true]}'
        -> {"ok":true,"type":"bool","value":false}

    A number written `1` and one written `1.0` are still the same value
    (`contains([1], 1.0)` -> `true`, also measured), so numbers are still
    compared by value; only the bool/number boundary is enforced. The same
    distinction holds inside nested collections, hence the recursion.
    """
    if isinstance(left, bool) != isinstance(right, bool):
        return False
    if isinstance(left, list | tuple) and isinstance(right, list | tuple):
        return len(left) == len(right) and all(
            _values_equal(item, other) for item, other in zip(left, right, strict=True)
        )
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(
            _values_equal(value, right[key]) for key, value in left.items()
        )
    return bool(left == right)


@register_function(name="length", summary="Returns the length of a given list, map, or string.")
def length(collection: list[Any] | dict[str, Any] | str | None) -> int | None:
    r"""Count a collection's elements, or a string's grapheme clusters.

    Terraform's `length` delegates the string case to go-cty's `strlen`, which
    counts UAX#29 extended grapheme clusters -- what a reader calls
    "characters" -- while this counted Python code points. Measured 2026-08-17
    with `soup-go cty call strlen`, the old answer from `len` on the left:

        family emoji, U+1F468 ZWJ U+1F469 ZWJ U+1F467 ZWJ U+1F466 -> was 7, is 1
        "e" followed by U+0301 COMBINING ACUTE ACCENT             -> was 2, is 1
        flag, U+1F1FA U+1F1F8 regional indicators                 -> was 2, is 1
        "hello"                                                   -> was 5, is 5

    Only the string branch changed: a list, map, set, tuple or object is still
    measured in elements. A value that is neither used to fail with Python's
    `object of type 'int' has no len()`; it now says which types are accepted,
    the way go-cty's own `length` ("collection must be a list, a map or a
    tuple") and `strlen` ("string required, but received number") do.
    """
    if collection is None:
        return None
    if isinstance(collection, str):
        result = grapheme_cluster_count(collection)
    elif isinstance(collection, _COLLECTION_TYPES):
        result = len(collection)
    else:
        raise FunctionError(
            f"Invalid argument for length: a list, a map, or a string is required, "
            f"but received {_cty_type_name(collection)}."
        )
    logger.debug(
        "Calculated collection length",
        collection_type=type(collection).__name__,
        length=result,
    )
    return result


@register_function(name="contains", summary="Checks if a list contains a given element.")
def contains(list_to_check: list[Any] | None, element: Any) -> bool | None:
    """Report whether the list holds a value equal to `element`.

    Compares with `_values_equal` rather than Python's `in`, so a bool no longer
    matches a number; see that helper for the measurements. 2026-08-17.
    """
    if list_to_check is None:
        return None
    result = any(_values_equal(candidate, element) for candidate in list_to_check)
    logger.debug("Checked list containment", list_length=len(list_to_check), found=result)
    return result


@register_function(name="lookup", summary="Performs a dynamic lookup into a map.")
@resilient()
def lookup(map_to_search: dict[str, Any] | None, key: str, *defaults: Any) -> Any:
    """
    Lookup a key in a map and return its value, or a default if the key doesn't exist.

    Using *defaults allows us to distinguish between:
    - lookup(map, key) - no default provided, should error if key missing
    - lookup(map, key, None) - default is None
    - lookup(map, key, False) - default is False
    - lookup(map, key, 0) - default is 0
    """
    if map_to_search is None:
        return None
    if key in map_to_search:
        logger.debug("Map lookup successful", key=key, map_size=len(map_to_search))
        return map_to_search[key]
    if defaults:  # Default was provided (even if falsy)
        default = defaults[0]
        logger.debug("Map lookup using default", key=key, has_default=True, default_value=default)
        return default
    logger.debug("Map lookup failed", key=key, available_keys=list(map_to_search.keys()))
    raise FunctionError(f'Invalid key for map lookup: key "{key}" does not exist in the map.')


# 🧩🔧🔚
