# pyvider/components/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# This file makes pyvider.components a package.
# Autodiscovery will scan from here.

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

# 🧩📦🔍
# 🧩🔧📦🪄
