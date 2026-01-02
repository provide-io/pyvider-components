# type: ignore
#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


"""Private state verifier resource for testing sensitive data handling."""

from typing import Any

from attrs import define, evolve

from pyvider.exceptions import ResourceError
from pyvider.hub import register_resource
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema, a_str, a_unknown, s_resource


@define(frozen=True)
class VerifierConfig:
    input_value: str


@define(frozen=True)
class VerifierState:
    input_value: str | None = None
    decrypted_token: str | None = None


@define(frozen=True)
class VerifierPrivateState(PrivateState):
    secret_token: str


@register_resource("pyvider_private_state_verifier", test_only=True)
class PrivateStateVerifierResource(BaseResource[VerifierState, VerifierState, VerifierConfig]):
    config_class = VerifierConfig
    state_class = VerifierState
    private_state_class = VerifierPrivateState

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "input_value": a_str(required=True),
                "decrypted_token": a_str(computed=True),
            }
        )

    async def _validate_config(self, config: VerifierConfig) -> list[str]:
        return []

    async def _create(  # type: ignore[override]
        self,
        ctx: ResourceContext[VerifierState, VerifierPrivateState],
        base_plan: dict[str, Any],
    ) -> tuple[dict[str, Any] | None, VerifierPrivateState | None]:
        base_plan["decrypted_token"] = a_unknown(a_str())
        # Handle None/unknown input_value at plan time (e.g., when using timestamp())
        input_val = ctx.config.input_value if ctx.config and ctx.config.input_value else ""
        assert self.private_state_class is not None
        private_state = self.private_state_class(secret_token=f"SECRET_FOR_{input_val.upper()}")
        return base_plan, private_state

    async def _create_apply(  # type: ignore[override]
        self, ctx: ResourceContext[VerifierState, VerifierPrivateState]
    ) -> tuple[VerifierState | None, VerifierPrivateState | None]:
        if not ctx.private_state:
            raise ResourceError("Apply phase failed: private state was not received.")

        assert ctx.planned_state is not None
        state: VerifierState = evolve(
            ctx.planned_state,
            decrypted_token=ctx.private_state.secret_token,
        )
        return state, None

    async def read(self, ctx: ResourceContext) -> VerifierState | None:  # type: ignore[type-arg]
        return ctx.state

    async def _delete_apply(self, ctx: ResourceContext) -> None:  # type: ignore[type-arg]
        pass


# 🧩🔧🔚
