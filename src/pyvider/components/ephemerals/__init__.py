#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Pyvider ephemeral resource components.

Components in this package register themselves with the
@register_ephemeral_resource decorator and are picked up by autodiscovery.
"""

__all__ = [
    # No explicit exports - autodiscovery handles registration
]

__component_type__ = "ephemeral_resource"
__autodiscovery__ = True

# 🧩🔧🔚
