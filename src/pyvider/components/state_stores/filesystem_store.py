#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A durable filesystem state store exposed as a Terraform state store type.

The storage, atomic writes, and lease-aware cross-process locking all live in
``pyvider.state_stores.FileSystemStateStore``. This module only gives that
backend a Terraform-facing type name and a configuration schema, so a
``state_store "pyvider_fs"`` block resolves to it.
"""

from __future__ import annotations

from typing import Any

from attrs import define

from pyvider.schema import PvsSchema, a_str, s_resource
from pyvider.state_stores import FileSystemStateStore, register_state_store


@define(frozen=True)
class FileSystemStoreConfig:
    path: str | None = None


@register_state_store("pyvider_fs", test_only=True)
class PyviderFileSystemStateStore(FileSystemStateStore):
    """``FileSystemStateStore`` with a Terraform configuration schema."""

    config_class = FileSystemStoreConfig

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
