#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from provide.foundation.utils.versioning import get_version

# Ensure provider is registered on import
from pyvider.components.provider import PyviderProvider
from pyvider.components.capabilities.core import CoreCapability

__version__ = get_version("pyvider-components", caller_file=__file__)

__all__ = [
    "__version__",
    "PyviderProvider",
    "CoreCapability",
]

# 🧩🔧🔚
