#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A durable filesystem state store exposed as a Terraform state store type.

The storage, atomic writes, and lease-aware cross-process locking all live in
``pyvider.state_stores.FileSystemStateStore``. This module only gives that
backend a Terraform-facing type name and a configuration schema, so a
``state_store "pyvider_filesystem_store"`` block resolves to it.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from attrs import define
from pyvider.lint import LintContext, LintFinding
from pyvider.schema import PvsSchema, a_str, s_resource
from pyvider.state_stores import FileSystemStateStore, register_state_store

from pyvider.components.lint_rules import ALL, RELATIVE_STATE_STORE_PATH, RELIABILITY


@define(frozen=True)
class FileSystemStoreConfig:
    path: str | None = None


@register_state_store("pyvider_filesystem_store")
class PyviderFileSystemStateStore(FileSystemStateStore):
    """``FileSystemStateStore`` with a Terraform configuration schema."""

    config_class = FileSystemStoreConfig

    async def lint(self, ctx: LintContext[FileSystemStoreConfig]) -> tuple[LintFinding, ...]:
        """Warn when state storage depends on the provider working directory."""
        if not ctx.enabled(RELATIVE_STATE_STORE_PATH, ALL, RELIABILITY):
            return ()
        path = getattr(ctx.config, "path", None)
        if path is None or getattr(path, "is_unknown", False) is True:
            return ()
        try:
            relative = not Path(str(path)).expanduser().is_absolute()
        except Exception:
            return ()
        if not relative:
            return ()
        return (
            LintFinding(
                rule=RELATIVE_STATE_STORE_PATH,
                groups=(ALL, RELIABILITY),
                summary="State store path is relative",
                detail=(
                    "A relative state store path may be intentional for a self-contained "
                    "workspace, but it depends on the provider process's working directory. "
                    "Set path to an absolute path for safer, predictable state storage. "
                    "Suppress with !provide-io/pyvider:relative-state-store-path."
                ),
                attribute_path="path",
            ),
        )

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "path": a_str(
                    required=True,
                    description=(
                        "Directory holding state for this store; created if absent. "
                        "A relative path resolves against the provider process's working "
                        "directory, which is not necessarily the one you ran Terraform from."
                    ),
                ),
            }
        )

    async def validate(self, config: Any) -> list[str]:
        errors = await super().validate(config)

        path = getattr(config, "path", None) if config is not None else None
        if path is None or not str(path).strip():
            errors.append("path is required")

        return errors


# 🧩🔧🔚
