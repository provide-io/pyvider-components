#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A list resource over real filesystem entries.

``pyvider_secret_note`` lists objects this provider process created, which
makes it deterministic but a little artificial. This one lists something that
genuinely exists outside the provider, which exercises the parts of the
contract the in-memory version cannot:

* it declares its **own** identity schema instead of borrowing one from a
  managed resource, which is the path a list resource takes when it has no
  managed counterpart;
* it emits **per-result warnings** for entries it can see but cannot stat,
  proving diagnostics ride along with individual results rather than aborting
  the stream;
* it yields lazily from a directory scan, so ``limit`` genuinely avoids work.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

from attrs import define

from pyvider.list_resources import (
    BaseListResource,
    ListResourceContext,
    ListResult,
    register_list_resource,
)
from pyvider.schema import PvsSchema, a_bool, a_num, a_str, s_identity, s_resource


@define(frozen=True)
class DirectoryEntriesConfig:
    path: str | None = None
    suffix: str | None = None
    include_hidden: bool | None = None


@define(frozen=True)
class DirectoryEntryState:
    path: str | None = None
    name: str | None = None
    size_bytes: int | None = None


@register_list_resource("pyvider_directory_entry", test_only=True)
class DirectoryEntryList(BaseListResource[DirectoryEntriesConfig]):
    """Lists files in a directory."""

    config_class = DirectoryEntriesConfig

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "path": a_str(required=True, description="Directory to list. Only read."),
                "suffix": a_str(description="Only return files ending with this."),
                "include_hidden": a_bool(description="Include dotfiles. Defaults to false."),
            }
        )

    @classmethod
    def get_identity_schema(cls) -> PvsSchema:
        """Declared here rather than borrowed: there is no managed counterpart."""
        return s_identity(attributes={"path": a_str(required=True)})

    @classmethod
    def get_resource_object_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "path": a_str(required=True),
                "name": a_str(required=True),
                "size_bytes": a_num(computed=True),
            }
        )

    async def validate(self, config: DirectoryEntriesConfig | None) -> list[str]:
        errors: list[str] = []
        if config is None or not config.path:
            errors.append("path is required")
            return errors

        candidate = Path(str(config.path)).expanduser()
        if candidate.exists() and not candidate.is_dir():
            errors.append(f"path '{candidate}' is not a directory")
        return errors

    async def list(self, ctx: ListResourceContext[DirectoryEntriesConfig]) -> AsyncIterator[ListResult]:
        assert ctx.config is not None
        root = Path(str(ctx.config.path)).expanduser()
        suffix = ctx.config.suffix or ""
        include_hidden = bool(ctx.config.include_hidden)

        if not root.is_dir():
            # An absent directory is an empty listing, not a failure: it may
            # simply not have been created yet.
            return

        for entry in sorted(root.iterdir()):
            # Name-based filters first: they answer without touching the disk,
            # so an entry that is filtered out is never stat-ed at all.
            if not include_hidden and entry.name.startswith("."):
                continue
            if suffix and not entry.name.endswith(suffix):
                continue

            warnings: tuple[str, ...] = ()
            size: int | None = None
            try:
                if not entry.is_file():
                    continue
                size = entry.stat().st_size
            except OSError as exc:
                # An entry `iterdir()` saw but that cannot be stat-ed is still
                # worth returning: it may have been removed, or had its
                # permissions changed, between the listing and the lookup, and
                # dropping it silently would misreport the directory. Letting
                # the error out is worse -- it fails the whole stream, so one
                # unreadable file hides every other one in the directory.
                warnings = (f"could not stat {entry.name}: {exc}",)

            resource_object = None
            if ctx.include_resource_object:
                resource_object = DirectoryEntryState(path=str(entry), name=entry.name, size_bytes=size)

            yield ListResult(
                identity={"path": str(entry)},
                display_name=entry.name,
                resource_object=resource_object,
                warnings=warnings,
            )


# 🧩🔧🔚
