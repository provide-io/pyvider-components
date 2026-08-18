#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Pyvider state_store components.

Components in this package register themselves with the @register_state_store
decorator and are picked up by autodiscovery.
"""

__all__ = [
    # No explicit exports - autodiscovery handles registration
]

__component_type__ = "state_store"
__autodiscovery__ = True

# 🧩🔧🔚
