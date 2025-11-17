#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from provide.foundation.utils.versioning import get_version

from pyvider.components.capabilities.core import CoreCapability

# Ensure provider is registered on import
from pyvider.components.provider import PyviderProvider

__version__ = get_version("pyvider-components", caller_file=__file__)

__all__ = [
    "CoreCapability",
    "PyviderProvider",
    "__version__",
]

# 🧩🔧🔚
