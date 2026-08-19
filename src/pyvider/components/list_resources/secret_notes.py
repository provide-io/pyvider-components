#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A demo list resource over ``pyvider_secret_note``.

Answers ``terraform query`` by streaming the notes this provider process knows
about. ``resource_type`` points at the managed resource, so identity and state
schemas are borrowed rather than restated.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

from attrs import define

from pyvider.components.resources.secret_note import SecretNoteState, known_notes
from pyvider.list_resources import (
    BaseListResource,
    ListResourceContext,
    ListResult,
    register_list_resource,
)
from pyvider.schema import PvsSchema, a_bool, a_str, s_resource


@define(frozen=True)
class SecretNoteListConfig:
    name_prefix: str | None = None
    include_archived: bool | None = None


@register_list_resource("pyvider_secret_note", resource_type="pyvider_secret_note", test_only=True)
class SecretNoteList(BaseListResource[SecretNoteListConfig]):
    """Lists the secret notes created in this provider process."""

    config_class = SecretNoteListConfig

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "name_prefix": a_str(description="Only return notes whose name starts with this."),
                "include_archived": a_bool(description="Reserved; accepted and ignored."),
            }
        )

    async def validate(self, config: SecretNoteListConfig | None) -> list[str]:
        if config is not None and config.name_prefix is not None and not config.name_prefix.strip():
            # An empty prefix is almost certainly a mistake -- it reads as a
            # filter but matches everything.
            return ["name_prefix must not be empty; omit it to list every note"]
        return []

    async def list(self, ctx: ListResourceContext[SecretNoteListConfig]) -> AsyncIterator[ListResult]:
        prefix = ctx.config.name_prefix if ctx.config and ctx.config.name_prefix else ""

        # known_notes() spans provider processes, so a note created by an
        # earlier `terraform apply` is listable from a later `terraform query`.
        notes = known_notes()
        for name in sorted(notes):
            if not name.startswith(prefix):
                continue

            resource_object = None
            if ctx.include_resource_object:
                # secret_value stays null even here: it is write-only, and a
                # list result is no more entitled to it than state is.
                resource_object = SecretNoteState(
                    name=name,
                    secret_value=None,
                    digest=notes[name],
                )

            yield ListResult(
                identity={"name": name},
                display_name=name,
                resource_object=resource_object,
            )


# 🧩🔧🔚
