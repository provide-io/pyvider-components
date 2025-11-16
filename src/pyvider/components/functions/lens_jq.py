#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from typing import Any

from pyvider.cty import CtyValue
from pyvider.cty.conversion import cty_to_native
from pyvider.exceptions import FunctionError
from pyvider.hub import register_function

from ..capabilities.lens import LensCapability


@register_function(name="lens_jq", component_of="lens")
def lens_jq(input_data: Any, query: str, *, lens: LensCapability) -> Any:
    """Applies a jq query and returns a native Python object."""

    if not lens.is_enabled:
        raise FunctionError(
            "The 'lens' capability is disabled in the provider configuration."
        )

    if not isinstance(query, str) or not query:
        raise FunctionError("The 'query' argument must be a non-empty string.")

    # Ensure input_data is converted to native Python before passing to JQ
    if isinstance(input_data, CtyValue):
        # If it's a CTY value, convert it to native Python first
        native_input_data = cty_to_native(input_data)
    else:
        # Assume it's already native Python data
        native_input_data = input_data

    try:
        result_cty = lens.jq(query, native_input_data)

        result = cty_to_native(result_cty)
        return result
    except Exception:
        raise


# 🧩🔧🔚
