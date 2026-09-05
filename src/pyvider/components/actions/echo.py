#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Demo actions used to exercise the tfprotov6.11 action RPCs end to end.

Actions are invoked by Terraform outside any resource lifecycle. These are
built to be run on the machine you are sitting at:

* they only ever append lines to a file you name, so there is nothing to undo;
* the side effect is verifiable (``cat`` the file), so a green apply is not the
  only evidence the action actually ran;
* each appended line is preceded by a progress event, which makes the streaming
  half of ``InvokeAction`` visible in the CLI rather than theoretical.

A demo action that *sounded* destructive but did nothing would be worse than
useless — nobody would run it, and if they did they would learn nothing.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from pathlib import Path

from attrs import define

from pyvider.actions import (
    ActionContext,
    ActionPlan,
    ActionProgress,
    BaseAction,
    DeferralReason,
    register_action,
)
from pyvider.schema import PvsSchema, a_bool, a_num, a_str, s_resource

#: Every line this process wrote, in order. Lets a test assert the action ran
#: without reaching for the filesystem.
WRITTEN: list[str] = []

#: Pause between steps so progress events are visible rather than instantaneous.
STEP_DELAY_SECONDS = 0.25


@define(frozen=True)
class EchoConfig:
    message: str | None = None
    path: str | None = None
    repeat: int | None = None
    #: Ask the action to defer instead of running. Terraform only accepts a
    #: deferral when it advertised deferral_allowed, so this makes the
    #: negotiation observable from a real CLI run.
    defer: bool | None = None


@register_action("pyvider_echo")
class EchoAction(BaseAction[EchoConfig]):
    """Appends a timestamped message to a file, reporting progress per line."""

    config_class = EchoConfig

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "message": a_str(required=True, description="Text to append."),
                "path": a_str(
                    required=True,
                    description="File to append to. Created if absent; nothing else is touched.",
                ),
                "repeat": a_num(description="How many lines to write. Must be positive."),
                "defer": a_bool(description="Defer instead of running, to exercise deferral."),
            }
        )

    async def validate(self, config: EchoConfig | None) -> list[str]:
        errors: list[str] = []
        if config is None or not config.message:
            errors.append("message is required")
        if config is None or not config.path:
            errors.append("path is required")
        if config is not None and config.repeat is not None and config.repeat < 1:
            errors.append("repeat must be a positive number")
        return errors

    async def plan(self, ctx: ActionContext[EchoConfig]) -> ActionPlan:
        if ctx.config is not None and ctx.config.defer:
            # The only reason Terraform accepts from PlanAction: "An action can
            # only be deferred due to an unknown provider configuration"
            # (internal/plugin6/grpc_provider.go:1951-1957). Every other reason
            # is an error there, so this knob would exercise nothing.
            return ActionPlan(defer=DeferralReason.PROVIDER_CONFIG_UNKNOWN)

        path = ctx.config.path if ctx.config else "?"
        return ActionPlan(warnings=(f"This will append to {path}.",))

    async def invoke(self, ctx: ActionContext[EchoConfig]) -> AsyncIterator[ActionProgress]:
        assert ctx.config is not None
        target = Path(str(ctx.config.path)).expanduser()
        repeat = int(ctx.config.repeat) if ctx.config.repeat else 1

        target.parent.mkdir(parents=True, exist_ok=True)

        for index in range(1, repeat + 1):
            suffix = f" ({index}/{repeat})" if repeat > 1 else ""
            yield ActionProgress(message=f"Writing to {target}{suffix}")

            stamp = datetime.now(UTC).isoformat(timespec="seconds")
            line = f"{stamp} {ctx.config.message}"
            with target.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
            WRITTEN.append(line)

            if STEP_DELAY_SECONDS:
                await asyncio.sleep(STEP_DELAY_SECONDS)

        yield ActionProgress(message=f"Wrote {repeat} line(s) to {target}")


@register_action("pyvider_failing_action", test_only=True)
class FailingAction(BaseAction[EchoConfig]):
    """Fails partway through, so the error path is observable from the CLI.

    A failure mid-stream must still produce exactly one completed event
    carrying the diagnostic; otherwise Terraform waits on an action that has
    already died.
    """

    config_class = EchoConfig

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(attributes={"message": a_str(required=True)})

    async def invoke(self, ctx: ActionContext[EchoConfig]) -> AsyncIterator[ActionProgress]:
        yield ActionProgress(message="Starting work that will not finish")
        raise RuntimeError("the remote system rejected the request")


# 🧩🔧🔚
