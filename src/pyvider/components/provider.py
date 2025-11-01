#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Provider implementation for pyvider-components.

This provides the reference implementation of a Pyvider provider,
managing standard components for local file manipulation,
HTTP data sources, and utility functions."""

from pyvider.providers import BaseProvider, ProviderMetadata, register_provider


@register_provider("pyvider")
class PyviderProvider(BaseProvider):
    """
    Reference implementation of a Pyvider provider.

    Manages standard components for local file manipulation,
    HTTP data sources, and utility functions.
    """

    def __init__(self):
        super().__init__(metadata=ProviderMetadata(name="pyvider", version="0.1.0"))


# 🧩🔧🔚
