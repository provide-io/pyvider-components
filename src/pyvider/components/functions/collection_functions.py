# 
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Any

from provide.foundation import logger
from provide.foundation.errors import resilient
from pyvider.exceptions import FunctionError
from pyvider.hub import register_function


@register_function(
    name="length", summary="Returns the length of a given list, map, or string."
)
def length(collection: list | dict | str | None) -> int | None:
    if collection is None:
        return None
    result = len(collection)
    logger.debug(
        "Calculated collection length",
        collection_type=type(collection).__name__,
        length=result,
    )
    return result


@register_function(
    name="contains", summary="Checks if a list contains a given element."
)
def contains(list_to_check: list[Any] | None, element: Any) -> bool | None:
    if list_to_check is None:
        return None
    result = element in list_to_check
    logger.debug(
        "Checked list containment", list_length=len(list_to_check), found=result
    )
    return result


@register_function(name="lookup", summary="Performs a dynamic lookup into a map.")
@resilient()
def lookup(map_to_search: dict[str, Any] | None, key: str, *defaults) -> Any:
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
        logger.debug(
            "Map lookup using default", key=key, has_default=True, default_value=default
        )
        return default
    logger.debug(
        "Map lookup failed", key=key, available_keys=list(map_to_search.keys())
    )
    raise FunctionError(
        f'Invalid key for map lookup: key "{key}" does not exist in the map.'
    )

# 🧩🔧🔚
