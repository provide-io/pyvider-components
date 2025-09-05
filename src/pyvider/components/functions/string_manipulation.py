#
# pyvider/components/functions/string_manipulation.py
#

from typing import Any

from pyvider.exceptions import FunctionError
from pyvider.hub import register_function
from provide.foundation import logger
from provide.foundation.errors import with_error_handling
from .type_conversion_functions import tostring


@register_function(name="upper", summary="Converts a string to uppercase.")
def upper(input_str: str | None) -> str | None:
    if input_str is None:
        return None
    return input_str.upper()


@register_function(name="lower", summary="Converts a string to lowercase.")
def lower(input_str: str | None) -> str | None:
    if input_str is None:
        return None
    return input_str.lower()


@register_function(
    name="format", summary="Formats a string using positional arguments."
)
@with_error_handling()
def format_str(template: str | None, values: list[Any] | None) -> str | None:
    if template is None:
        return None
    value_list = values or []
    try:
        str_values = [tostring(v) for v in value_list]
        result = template.format(*str_values)
        logger.debug(f"Formatted string with template '{template}' and {len(value_list)} values")
        return result
    except IndexError as e:
        raise FunctionError(
            f"Formatting failed: not enough values for template '{template}'."
        ) from e


@register_function(name="join", summary="Joins list elements with a delimiter.")
def join(delimiter: str | None, strings: list[Any] | None) -> str | None:
    if strings is None:
        return None
    delimiter_str = delimiter or ""
    return delimiter_str.join(map(tostring, strings))


@register_function(name="split", summary="Splits a string by a delimiter.")
def split(delimiter: str | None, string: str | None) -> list[str] | None:
    if string is None:
        return None
    delimiter_str = delimiter or ""
    if not string:
        return []
    return string.split(delimiter_str)


@register_function(name="replace", summary="Replaces occurrences of a substring.")
def replace(
    string: str | None, search: str | None, replacement: str | None
) -> str | None:
    if string is None:
        return None
    return string.replace(search or "", replacement or "")


# ✂️📝🎯
