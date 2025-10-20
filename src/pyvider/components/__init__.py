# pyvider/components/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# This file makes pyvider.components a package.
# Autodiscovery will scan from here.

from provide.foundation.utils.versioning import get_version

__version__ = get_version("pyvider-components", caller_file=__file__)

__all__ = [
    "__version__",
]

# 🧩📦🔍
# 🧩🔧📦🪄
