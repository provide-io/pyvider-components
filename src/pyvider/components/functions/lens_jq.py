#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


"""JQ lens function for JSON querying and transformation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..capabilities.lens import LensCapability

from pyvider.cty import CtyValue
from pyvider.cty.conversion import cty_to_native
from pyvider.exceptions import FunctionError
from pyvider.hub import register_function


@register_function(name="lens_jq", component_of="lens")
def lens_jq(input_data: Any, query: str, *, lens: LensCapability) -> Any:
    """Applies a jq query and returns a native Python object."""

    if not lens.is_enabled:
        raise FunctionError("The 'lens' capability is disabled in the provider configuration.")

    if not isinstance(query, str) or not query:
        raise FunctionError("The 'query' argument must be a non-empty string.")

    # Ensure input_data is converted to native Python before passing to JQ
    native_input_data = cty_to_native(input_data) if isinstance(input_data, CtyValue) else input_data

    try:
        result_cty = lens.jq(query, native_input_data)

        result = cty_to_native(result_cty)
        return result
    except Exception:
        raise


# 🧩🔧🔚
