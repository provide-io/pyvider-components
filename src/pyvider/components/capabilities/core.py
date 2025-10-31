# 
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Core capability for the pyvider provider.

Provides base provider configuration for the pyvider-components package."""

from typing import Any

from pyvider.capabilities import BaseCapability, register_capability
from pyvider.schema import PvsAttribute, a_bool


@register_capability("core")
class CoreCapability(BaseCapability):
    """
    Core capability for pyvider provider.
    Provides base provider configuration (currently empty).
    """

    def __init__(self, config: Any | None = None):
        pass

    @staticmethod
    def get_schema_contribution() -> dict[str, PvsAttribute]:
        """
        Return the schema contribution for this capability.

        Provides:
        - provider_testmode: Enables test-only components for testing and development
        """
        return {
            "provider_testmode": a_bool(
                optional=True,
                default=False,
                description="Enable test-only components for testing and development purposes.",
            )
        }

# 🧩🔧🔚
