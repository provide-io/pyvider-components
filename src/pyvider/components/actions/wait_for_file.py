#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""An action that waits for a file, demonstrating deferral and long-running work.

Where ``pyvider_echo`` shows the ordinary path, this one covers the two shapes
an action can take that are easy to get wrong:

* **Deferral.** If the file is not there yet, planning returns
  ``ABSENT_PREREQ`` rather than failing. That is exactly what a deferral is
  for: the operation is not wrong, it is not answerable yet.
* **Genuinely long work.** Progress events are emitted while polling, so the
  practitioner sees movement instead of a silent stall.

Safe to run locally: it only reads, and gives up after its own timeout.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncIterator
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
from pyvider.schema import PvsSchema, a_num, a_str, s_resource

DEFAULT_TIMEOUT_SECONDS = 10.0
POLL_INTERVAL_SECONDS = 0.1


@define(frozen=True)
class WaitForFileConfig:
    path: str | None = None
    timeout_seconds: float | None = None


@register_action("pyvider_wait_for_file")
class WaitForFileAction(BaseAction[WaitForFileConfig]):
    """Blocks until a path exists, reporting progress while it waits."""

    config_class = WaitForFileConfig

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            attributes={
                "path": a_str(required=True, description="Path to wait for. Only read, never written."),
                "timeout_seconds": a_num(description="How long to wait before failing."),
            }
        )

    async def validate(self, config: WaitForFileConfig | None) -> list[str]:
        errors: list[str] = []
        if config is None or not config.path:
            errors.append("path is required")
        if config is not None and config.timeout_seconds is not None and config.timeout_seconds <= 0:
            errors.append("timeout_seconds must be greater than zero")
        return errors

    async def plan(self, ctx: ActionContext[WaitForFileConfig]) -> ActionPlan:
        assert ctx.config is not None
        target = Path(str(ctx.config.path)).expanduser()

        if not target.exists():
            # Not an error: the file may well be created by something else in
            # this same run. Deferring says "ask me again", which is the honest
            # answer and the reason the protocol has deferrals at all.
            return ActionPlan(defer=DeferralReason.ABSENT_PREREQ)

        return ActionPlan()

    async def invoke(self, ctx: ActionContext[WaitForFileConfig]) -> AsyncIterator[ActionProgress]:
        assert ctx.config is not None
        target = Path(str(ctx.config.path)).expanduser()
        timeout = float(ctx.config.timeout_seconds or DEFAULT_TIMEOUT_SECONDS)
        deadline = time.monotonic() + timeout

        waited = 0
        while not target.exists():
            if time.monotonic() >= deadline:
                raise TimeoutError(f"{target} did not appear within {timeout} seconds")
            if waited % 5 == 0:
                yield ActionProgress(message=f"Waiting for {target}")
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
            waited += 1

        yield ActionProgress(message=f"{target} exists")


# 🧩🔧🔚
