#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Pyvider Data Sources Components
==============================
This package contains all data source components that are automatically discovered
and registered by the Pyvider framework.

Components in this package must use the @register_data_source decorator."""

__all__ = [
    # No explicit exports - autodiscovery handles registration
]

# Metadata for the autodiscovery system
__component_type__ = "data_source"
__autodiscovery__ = True

# 🧩🔧🔚
