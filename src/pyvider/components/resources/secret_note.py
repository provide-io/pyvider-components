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
import json
import os
import tempfile
from pathlib import Path
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

#: Where the durable index of notes lives. A real provider talks to a system
#: that outlives the process; this file stands in for it. Without one, `list`
#: and `import` are unusable from the CLI: Terraform starts a fresh provider
#: process per command, so a note created by `apply` is invisible to the
#: `query` or `import` that follows.
NOTE_INDEX_ENV = "PYVIDER_SECRET_NOTE_INDEX"
DEFAULT_NOTE_INDEX = Path(tempfile.gettempdir()) / "pyvider-secret-notes.json"

DIGEST_LENGTH = 16


def note_index_path() -> Path:
    """Resolve the durable index location, honouring the environment."""
    override = os.environ.get(NOTE_INDEX_ENV)
    return Path(override) if override else DEFAULT_NOTE_INDEX


def _load_index() -> dict[str, str]:
    """Read the durable index, treating any damage as "no notes".

    A demo resource must not make a mangled scratch file fatal to a whole
    Terraform run, and the index is reconstructible by re-applying.
    """
    path = note_index_path()
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(loaded, dict):
        return {}
    return {str(name): str(digest) for name, digest in loaded.items()}


def _save_index(notes: dict[str, str]) -> None:
    """Replace the index atomically so a concurrent reader sees whole content."""
    path = note_index_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(notes, handle)
        Path(tmp_name).replace(path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise


def record_note(name: str, digest: str) -> None:
    """Publish a note so later provider processes can see it.

    Only the digest is stored. ``secret_value`` is write-only: persisting it
    here would recreate exactly the leak the attribute exists to prevent.
    """
    notes = _load_index()
    notes[name] = digest
    _save_index(notes)


def forget_note(name: str) -> None:
    """Drop a note from the durable index."""
    notes = _load_index()
    if notes.pop(name, None) is not None:
        _save_index(notes)


def known_notes() -> dict[str, str]:
    """Every note this provider can see, as name -> digest.

    Notes created in this process win: they are the freshest, and during a
    single apply they exist before the index write is observable elsewhere.
    """
    notes = _load_index()
    notes.update({name: digest_of(secret) for name, secret in _NOTES.items()})
    return notes


def digest_of(secret: str) -> str:
    """Derive the public digest a practitioner can safely see in state."""
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()[:DIGEST_LENGTH]


@define(frozen=True)
class SecretNoteConfig:
    name: str | None = None
    secret_value: str | None = None
    secret_version: str | None = None


@define(frozen=True)
class SecretNoteState:
    name: str | None = None
    secret_value: str | None = None
    secret_version: str | None = None
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
                "secret_version": a_str(
                    description=(
                        "Change this to tell the provider secret_value changed. "
                        "Write-only values are absent from prior state, so a change "
                        "to one cannot be detected by comparison."
                    ),
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
        return SecretNoteConfig(
            name=getattr(state, "name", None),
            secret_value=None,
            secret_version=getattr(state, "secret_version", None),
        )

    async def _validate_config(self, config: SecretNoteConfig) -> list[str]:
        errors: list[str] = []
        if config.name is not None and not config.name.strip():
            errors.append("name must not be empty")
        if config.secret_value is not None and not config.secret_value:
            errors.append("secret_value must not be empty")
        return errors

    def _planned_digest(self, ctx: ResourceContext[SecretNoteConfig, SecretNoteState, Any]) -> Any:
        """Plan the digest for an *update*, without re-deriving it every time.

        A write-only value is absent from prior state, so the provider cannot
        tell a changed secret from an unchanged one by comparing. Two obvious
        approaches are both wrong:

        * always mark the digest unknown -- every plan after an apply then
          reports a change to a note nobody touched, so the configuration never
          converges and a real change is lost in the noise;
        * always re-derive it from the config -- the digest becomes a plan-time
          value derived from a write-only input, and write-only inputs are
          exactly where ephemeral values belong. An ephemeral value differs
          between plan and apply by design, so Terraform rejects the result:
          "Provider produced inconsistent final plan".

        The trigger attribute is Terraform's answer: the practitioner says when
        the secret changed, and only then is the digest unknown.
        """
        prior_digest = getattr(ctx.state, "digest", None)
        prior_version = getattr(ctx.state, "secret_version", None)
        version = ctx.config.secret_version if ctx.config is not None else None

        if prior_digest is None or version != prior_version:
            return a_unknown(a_str())
        return prior_digest

    async def _create(
        self,
        ctx: ResourceContext[SecretNoteConfig, SecretNoteState, Any],
        base_plan: dict[str, Any],
    ) -> tuple[dict[str, Any] | None, Any]:
        # Unknown on create, always: the secret may be an ephemeral value, which
        # differs between plan and apply by design. There is nothing to converge
        # on yet either, so this costs nothing.
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
        record_note(name, digest_of(secret))

        assert ctx.planned_state is not None
        return (
            evolve(
                ctx.planned_state,
                digest=digest_of(secret),
                secret_version=ctx.config.secret_version if ctx.config else None,
            ),
            None,
        )

    async def _update(
        self,
        ctx: ResourceContext[SecretNoteConfig, SecretNoteState, Any],
        base_plan: dict[str, Any],
    ) -> tuple[dict[str, Any] | None, Any]:
        base_plan["digest"] = self._planned_digest(ctx)
        return base_plan, None

    async def _update_apply(
        self, ctx: ResourceContext[SecretNoteConfig, SecretNoteState, Any]
    ) -> tuple[SecretNoteState | None, Any]:
        return await self._create_apply(ctx)

    async def import_state(self, ctx: ResourceContext, import_id: str) -> SecretNoteState | None:  # type: ignore[type-arg]
        """Adopt a note that already exists into state.

        Terraform can address the object by an import id or by resource
        identity, and sends whichever the practitioner used. Identity wins when
        both arrive: it is the structured form, and the id is free text.

        ``secret_value`` stays null. It is write-only, so it was never stored
        and cannot be recovered from the remote object; inventing a value here
        would put a fabricated secret into state.
        """
        name = import_id
        identity = getattr(ctx, "identity", None)
        if identity:
            name = identity.get("name") or import_id

        digest = known_notes().get(name)
        if digest is None:
            # Returning None is how a resource says "no such object", which
            # Terraform reports differently from "cannot import at all".
            return None

        return SecretNoteState(name=name, secret_value=None, digest=digest)

    async def read(self, ctx: ResourceContext) -> SecretNoteState | None:  # type: ignore[type-arg]
        # secret_value stays null: it is write-only and was never persisted.
        state: SecretNoteState | None = ctx.state
        return state

    async def _delete_apply(self, ctx: ResourceContext) -> None:  # type: ignore[type-arg]
        name = getattr(ctx.state, "name", None)
        if name:
            _NOTES.pop(name, None)
            forget_note(name)


# 🧩🔧🔚
