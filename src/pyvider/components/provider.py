#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Provider implementation for pyvider-components.

This provides the reference implementation of a Pyvider provider,
managing standard components for local file manipulation,
HTTP data sources, and utility functions."""

from typing import Any

from pyvider.lint import LintContext, LintFinding
from pyvider.providers import BaseProvider, ProviderMetadata, register_provider

from pyvider.components.lint_rules import ALL, INSECURE_TLS, SECURITY


@register_provider("pyvider")
class PyviderProvider(BaseProvider):
    """
    Reference implementation of a Pyvider provider.

    Manages standard components for local file manipulation,
    HTTP data sources, and utility functions.
    """

    def __init__(self) -> None:
        super().__init__(metadata=ProviderMetadata(name="pyvider", version="0.1.0"))

    async def lint(self, ctx: LintContext[Any]) -> tuple[LintFinding, ...]:
        """Warn when provider TLS verification is explicitly disabled."""
        if not ctx.enabled(INSECURE_TLS, ALL, SECURITY):
            return ()
        if getattr(ctx.config, "api_insecure_skip_verify", None) is not True:
            return ()
        return (
            LintFinding(
                rule=INSECURE_TLS,
                groups=(ALL, SECURITY),
                summary="TLS certificate verification is disabled",
                detail=(
                    "Skipping TLS certificate verification may be intentional for local "
                    "development, but it permits man-in-the-middle attacks. Set "
                    "api_insecure_skip_verify to false for safer connections. Suppress with "
                    "!provide-io/pyvider:insecure-tls."
                ),
                attribute_path="api_insecure_skip_verify",
            ),
        )


# 🧩🔧🔚
