#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A note with a write-only secret, used to exercise tfprotov6.11 end to end.

This resource is the anchor for the v6.11 CLI fixtures. It exists to make three
protocol behaviours observable from a real Terraform run:

* ``secret_value`` is ``write_only``: it must be usable while applying and must
  come back null from state afterwards.
* ``digest`` is computed from ``secret_value`` provider-side, which proves the
  secret actually reached the provider rather than being dropped on the way in.
* ``name`` is the resource identity, so import and list results have something
  to key on.
"""

from __future__ import annotations

import hashlib
from typing import Any

from attrs import define, evolve

from pyvider.hub import register_resource
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.schema import PvsSchema, a_str, a_unknown, s_identity, s_resource

#: Notes created during a run, keyed by name. A demo resource has no remote
#: system to talk to; this stands in for one so read/list have something to
#: return within a single provider process.
_NOTES: dict[str, str] = {}

DIGEST_LENGTH = 16


def digest_of(secret: str) -> str:
    """Derive the public digest a practitioner can safely see in state."""
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()[:DIGEST_LENGTH]


@define(frozen=True)
class SecretNoteConfig:
    name: str | None = None
    secret_value: str | None = None


@define(frozen=True)
class SecretNoteState:
    name: str | None = None
    secret_value: str | None = None
    digest: str | None = None


@register_resource("pyvider_secret_note", test_only=True)
class SecretNoteResource(BaseResource[SecretNoteState, SecretNoteState, SecretNoteConfig]):
    config_class = SecretNoteConfig
    state_class = SecretNoteState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "name": a_str(required=True, description="Identifier for the note."),
                "secret_value": a_str(
                    required=True,
                    write_only=True,
                    description="Never persisted to state; only the digest is.",
                ),
                "digest": a_str(computed=True, description="Digest derived from secret_value."),
            }
        )

    @classmethod
    def get_identity_schema(cls) -> PvsSchema:
        return s_identity(attributes={"name": a_str(required=True)})

    async def generate_config(self, state: Any) -> Any:
        """Drop computed attributes so the result is a writable configuration.

        ``digest`` is computed, so echoing it back would produce a config
        Terraform rejects. ``secret_value`` cannot be recovered from state by
        design, so generated config leaves it unset for a human to fill in.
        """
        if state is None:
            return None
        return SecretNoteConfig(name=getattr(state, "name", None), secret_value=None)

    async def _validate_config(self, config: SecretNoteConfig) -> list[str]:
        errors: list[str] = []
        if config.name is not None and not config.name.strip():
            errors.append("name must not be empty")
        if config.secret_value is not None and not config.secret_value:
            errors.append("secret_value must not be empty")
        return errors

    async def _create(
        self,
        ctx: ResourceContext[SecretNoteConfig, SecretNoteState, Any],
        base_plan: dict[str, Any],
    ) -> tuple[dict[str, Any] | None, Any]:
        base_plan["digest"] = a_unknown(a_str())
        return base_plan, None

    async def _create_apply(
        self, ctx: ResourceContext[SecretNoteConfig, SecretNoteState, Any]
    ) -> tuple[SecretNoteState | None, Any]:
        secret = ctx.config.secret_value if ctx.config else None
        if not secret:
            # Reaching apply without the write-only value means it was stripped
            # inbound, which is the exact regression this resource guards.
            raise ValueError(
                "secret_value was not delivered to the provider during apply; "
                "write-only attributes must survive the inbound boundary."
            )

        name = ctx.config.name if ctx.config else None
        assert name is not None
        _NOTES[name] = secret

        assert ctx.planned_state is not None
        return evolve(ctx.planned_state, digest=digest_of(secret)), None

    async def _update(
        self,
        ctx: ResourceContext[SecretNoteConfig, SecretNoteState, Any],
        base_plan: dict[str, Any],
    ) -> tuple[dict[str, Any] | None, Any]:
        base_plan["digest"] = a_unknown(a_str())
        return base_plan, None

    async def _update_apply(
        self, ctx: ResourceContext[SecretNoteConfig, SecretNoteState, Any]
    ) -> tuple[SecretNoteState | None, Any]:
        return await self._create_apply(ctx)

    async def read(self, ctx: ResourceContext) -> SecretNoteState | None:  # type: ignore[type-arg]
        # secret_value stays null: it is write-only and was never persisted.
        state: SecretNoteState | None = ctx.state
        return state

    async def _delete_apply(self, ctx: ResourceContext) -> None:  # type: ignore[type-arg]
        name = getattr(ctx.state, "name", None)
        if name:
            _NOTES.pop(name, None)


# 🧩🔧🔚
