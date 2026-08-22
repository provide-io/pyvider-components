#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""A demo ephemeral resource, to exercise the ephemeral RPCs end to end.

Ephemeral resources exist for values that must not be persisted: a session
token, a short-lived credential, a connection. Terraform opens one, renews it
for as long as the run needs it, and closes it -- and none of it reaches state.

This one takes out a *lease* on a file, so the whole lifecycle leaves a trail
you can read afterwards:

* ``open`` writes the lease file, so an opened lease is visible on disk;
* ``renew`` appends to it, so renewals are countable rather than assumed;
* ``close`` deletes it, so a leaked lease is obvious -- a file that is still
  there after a run is a close that never happened.

A demo that only returned a value would prove the RPCs were *called*, not that
the provider did the work between them.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from pathlib import Path

from attrs import define

from pyvider.ephemerals import (
    BaseEphemeralResource,
    EphemeralResourceContext,
    register_ephemeral_resource,
)
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema, a_num, a_str, s_resource

#: Default lease duration. Short enough that a run of any length renews at
#: least once, which is the half of the contract that otherwise goes untested.
DEFAULT_TTL_SECONDS = 30


@define(frozen=True)
class LeaseConfig:
    name: str | None = None
    path: str | None = None
    ttl_seconds: int | None = None


@define(frozen=True)
class LeaseResult:
    name: str | None = None
    path: str | None = None
    #: Echoed back from config. Every attribute the schema lets a practitioner set
    #: has to come back unchanged, or Terraform rejects the whole resource with
    #: "planned value does not match config value" -- a field missing here reads
    #: as the provider returning null for something the configuration set.
    ttl_seconds: int | None = None
    lease_id: str | None = None
    expires_at: str | None = None


@define(frozen=True)
class LeasePrivateState(PrivateState):
    lease_id: str = ""
    path: str = ""
    ttl_seconds: int = DEFAULT_TTL_SECONDS
    renewals: int = 0


@register_ephemeral_resource("pyvider_lease", test_only=True)
class LeaseEphemeralResource(BaseEphemeralResource[LeaseResult, LeasePrivateState, LeaseConfig]):
    """Holds a lease on a file for as long as Terraform needs it."""

    config_class = LeaseConfig
    result_class = LeaseResult
    private_state_class = LeasePrivateState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "name": a_str(required=True, description="Identifier for the lease."),
                "path": a_str(
                    required=True,
                    description="Lease file to hold. Created on open and removed on close.",
                ),
                "ttl_seconds": a_num(description="Lease duration before Terraform must renew."),
                "lease_id": a_str(computed=True, description="Identifier issued when the lease opened."),
                "expires_at": a_str(computed=True, description="When the current lease expires (UTC)."),
            }
        )

    async def validate(self, config: LeaseConfig | None) -> list[str]:
        errors: list[str] = []
        if config is None or not config.name:
            errors.append("name is required")
        if config is None or not config.path:
            errors.append("path is required")
        if config is not None and config.ttl_seconds is not None and config.ttl_seconds < 1:
            errors.append("ttl_seconds must be a positive number")
        return errors

    def _lease_file(self, path: str) -> Path:
        return Path(path).expanduser()

    async def open(
        self,
        ctx: EphemeralResourceContext[LeaseConfig, None],  # type: ignore[type-var]
    ) -> tuple[LeaseResult, LeasePrivateState, datetime]:
        assert ctx.config is not None
        ttl = int(ctx.config.ttl_seconds) if ctx.config.ttl_seconds else DEFAULT_TTL_SECONDS
        lease_id = str(uuid.uuid4())
        target = self._lease_file(str(ctx.config.path))
        expires_at = datetime.now(UTC) + timedelta(seconds=ttl)

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"opened {lease_id} for {ctx.config.name}\n", encoding="utf-8")

        return (
            LeaseResult(
                # Echo the configured path back verbatim. Returning the resolved
                # form instead ("./held.lease" -> "held.lease") is a different
                # value as far as Terraform is concerned, and it rejects the
                # whole resource: "planned value does not match config value".
                # The resolved path is kept in private state, where it is the
                # provider's own business.
                name=ctx.config.name,
                path=ctx.config.path,
                # Verbatim, not the defaulted `ttl` below it: when the config omits
                # ttl_seconds the returned value has to stay null too, or the same
                # consistency check fails in the other direction. DEFAULT_TTL_SECONDS
                # governs the lease itself and lives in private state.
                ttl_seconds=ctx.config.ttl_seconds,
                lease_id=lease_id,
                expires_at=expires_at.isoformat(timespec="seconds"),
            ),
            LeasePrivateState(lease_id=lease_id, path=str(target), ttl_seconds=ttl, renewals=0),
            expires_at,
        )

    async def renew(
        self, ctx: EphemeralResourceContext[None, LeasePrivateState]
    ) -> tuple[LeasePrivateState, datetime]:
        assert ctx.private_state is not None
        state = ctx.private_state
        renewals = state.renewals + 1
        expires_at = datetime.now(UTC) + timedelta(seconds=state.ttl_seconds)

        target = self._lease_file(state.path)
        if target.exists():
            # Appending rather than rewriting: the count of renewals is the
            # evidence that renew actually ran, not merely returned.
            with target.open("a", encoding="utf-8") as handle:
                handle.write(f"renewed {state.lease_id} #{renewals}\n")

        return (
            LeasePrivateState(
                lease_id=state.lease_id,
                path=state.path,
                ttl_seconds=state.ttl_seconds,
                renewals=renewals,
            ),
            expires_at,
        )

    async def close(self, ctx: EphemeralResourceContext[None, LeasePrivateState]) -> None:
        assert ctx.private_state is not None
        # Removing the file is the whole point: a lease still on disk after a
        # run is a close that never happened.
        self._lease_file(ctx.private_state.path).unlink(missing_ok=True)


# 🧩🔧🔚
