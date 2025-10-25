# pyvider/components/capabilities/core.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""
Core capability for the pyvider provider.

Provides base provider configuration for the pyvider-components package.
"""

from typing import Any

from pyvider.capabilities import BaseCapability, register_capability
from pyvider.schema import PvsAttribute


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
        Currently returns an empty dict as the core capability
        has no additional configuration requirements.
        """
        return {}