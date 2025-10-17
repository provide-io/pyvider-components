#
# pyvider/components/functions/string_manipulation.py
#

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
from pyvider.exceptions import FunctionError
from pyvider.hub import register_function

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
@resilient()
def format_str(template: str | None, values: list[Any] | None) -> str | None:
    if template is None:
        return None
    value_list = values or []
    try:
        str_values = [tostring(v) for v in value_list]
        result = template.format(*str_values)
        logger.debug("Formatted string", template=template, value_count=len(value_list))
        return result
    except IndexError as e:
        raise FunctionError(
            f"Formatting failed: not enough values for template '{template}'."
        ) from e


@register_function(name="join", summary="Joins list elements with a delimiter.")
def join(strings: list[Any] | None, delimiter: str | None) -> str | None:
    if strings is None:
        return None
    delimiter_str = delimiter or ""
    return delimiter_str.join(map(tostring, strings))


@register_function(name="split", summary="Splits a string by a delimiter.")
def split(string: str | None, delimiter: str | None) -> list[str] | None:
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
def camel_case(text: str | None, *options) -> str | None:
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
def format_file_size(size_bytes: int | None, *options) -> str | None:
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
def truncate_text(text: str | None, *options) -> str | None:
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
def pluralize_word(word: str | None, *options) -> str | None:
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

    return pluralize(word, count, plural)


# ✂️📝🎯
