#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A list resource over real files on disk.

``pyvider_secret_note`` lists objects this provider process created, which
makes it deterministic but a little artificial. This one lists something that
genuinely exists outside the provider, which exercises the parts of the
contract the in-memory version cannot:

* it emits **per-result warnings** for entries it can see but cannot read,
  proving diagnostics ride along with individual results rather than aborting
  the stream;
* it yields lazily from a directory scan, so ``limit`` genuinely avoids work.

It lists what ``pyvider_file_content`` manages, and takes that resource's name.
Terraform resolves a list resource against the managed type of the same name
and refuses to list one that has none
(terraform/internal/plugin6/grpc_provider.go:1341-1345); it then decodes each
result's identity and resource object against that managed resource's schemas
(:1420-1436), so neither shape is this class's to describe. ``resource_type``
borrows both.
"""

from __future__ import annotations

import hashlib
from collections.abc import AsyncIterator
from pathlib import Path

from attrs import define

from pyvider.list_resources import (
    BaseListResource,
    ListResourceContext,
    ListResult,
    register_list_resource,
)
from pyvider.schema import PvsSchema, a_bool, a_str, s_resource


@define(frozen=True)
class DirectoryEntriesConfig:
    path: str | None = None
    suffix: str | None = None
    include_hidden: bool | None = None


@register_list_resource("pyvider_file_content", resource_type="pyvider_file_content")
class FileContentList(BaseListResource[DirectoryEntriesConfig]):
    """Lists the files in a directory as `pyvider_file_content` resources."""

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
            content: str | None = None
            try:
                if not entry.is_file():
                    continue
                # Reading is deferred to the point it is asked for: a listing
                # that only wants identities never opens a file.
                if ctx.include_resource_object:
                    content = entry.read_text()
            except OSError as exc:
                # An entry `iterdir()` saw but that cannot be read is still
                # worth returning: it may have been removed, or had its
                # permissions changed, between the listing and the lookup, and
                # dropping it silently would misreport the directory. Letting
                # the error out is worse -- it fails the whole stream, so one
                # unreadable file hides every other one in the directory.
                warnings = (f"could not read {entry.name}: {exc}",)
            except UnicodeDecodeError as exc:
                # `content` is a string attribute, so a binary file has no
                # value to report. The file is still listed, and still
                # importable by identity.
                warnings = (f"{entry.name} is not text: {exc}",)

            # Shaped by `pyvider_file_content`'s own schema, which is what
            # Terraform decodes a listed resource object against -- "Use the
            # ResourceTypes schema for the resource object"
            # (terraform/internal/plugin6/grpc_provider.go:1428-1431). The
            # framework supplies that schema through `resource_type`, so this
            # only has to fill it.
            resource_object = None
            if ctx.include_resource_object and content is not None:
                resource_object = {
                    "filename": str(entry),
                    "content": content,
                    "exists": True,
                    "content_hash": hashlib.sha256(content.encode()).hexdigest(),
                }

            yield ListResult(
                identity={"filename": str(entry)},
                display_name=entry.name,
                resource_object=resource_object,
                warnings=warnings,
            )


# 🧩🔧🔚
