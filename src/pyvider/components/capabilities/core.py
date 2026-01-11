#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
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

    def __init__(self, config: Any | None = None) -> None:
        self.config = config

    @staticmethod
    def get_schema_contribution() -> dict[str, PvsAttribute]:
        """
        Return the schema contribution for this capability.

        Provides:
        - pyvider_testmode: Enables test-only components for testing and development
        """
        return {
            "pyvider_testmode": a_bool(
                optional=True,
                default=False,
                description="Enable test-only components for testing and development purposes.",
            )
        }


# 🧩🔧🔚
