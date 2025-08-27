#
# pyvider/components/functions/type_conversion_functions.py
#

from typing import Any

from pyvider.hub import register_function


@register_function(name="tostring", summary="Explicitly converts a value to a string.")
def tostring(value: Any | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


# 🔄🏷️🎯
