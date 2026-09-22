#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""An action that waits for a file, demonstrating long-running work.

Where ``pyvider_echo`` shows the ordinary path, this one covers the shape that
is easy to get wrong: **genuinely long work**. Progress events are emitted while
polling, so the practitioner sees movement instead of a silent stall.

A missing file is reported at plan time as a warning and waited for in
``invoke``. It is deliberately not a deferral: Terraform accepts an action
deferral only for an unknown provider configuration, so a prerequisite that has
not appeared yet has no deferral to express. ``pyvider_echo`` carries the
deferral demonstration instead.

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
    register_action,
)
from pyvider.lint import LintContext, LintFinding
from pyvider.schema import PvsSchema, a_num, a_str, s_resource

from pyvider.components.lint_rules import ALL, LONG_ACTION_TIMEOUT, RELIABILITY

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

    async def lint(self, ctx: LintContext[WaitForFileConfig]) -> tuple[LintFinding, ...]:
        """Warn when an action may wait for more than five minutes."""
        if not ctx.enabled(LONG_ACTION_TIMEOUT, ALL, RELIABILITY):
            return ()
        timeout_seconds = getattr(ctx.config, "timeout_seconds", None)
        try:
            long_timeout = timeout_seconds is not None and timeout_seconds > 300
        except Exception:
            return ()
        if not long_timeout:
            return ()
        return (
            LintFinding(
                rule=LONG_ACTION_TIMEOUT,
                groups=(ALL, RELIABILITY),
                summary="Action timeout exceeds five minutes",
                detail=(
                    "A timeout longer than five minutes may be intentional for slow "
                    "prerequisites, but it can leave Terraform waiting for an unresponsive "
                    "action. Set timeout_seconds to 300 or less for a safer timeout. Suppress "
                    "with !provide-io/pyvider:long-action-timeout."
                ),
                attribute_path="timeout_seconds",
            ),
        )

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
        # An empty config decodes to None, and the handler turns anything raised
        # here into an ERROR carrying the exception's message -- empty, for an
        # assert. Naming the missing attribute is what `validate` already does.
        if ctx.config is None or not ctx.config.path:
            raise ValueError("path is required")

        target = Path(str(ctx.config.path)).expanduser()

        # An absent file is not planned around. Terraform accepts exactly one
        # reason for deferring an action -- "the provider must be able to accept
        # unknown configuration" (internal/plugin6/grpc_provider.go:1940-1957) --
        # and a missing file is not that, so saying so would be both refused and
        # untrue. Waiting is what this action is for, and `invoke` does it:
        # polling until the file appears or `timeout_seconds` elapses.
        if not target.exists():
            return ActionPlan(warnings=(f"{target} does not exist yet; the action will wait for it.",))

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
