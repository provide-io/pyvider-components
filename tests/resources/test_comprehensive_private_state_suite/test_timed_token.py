#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test the fixed TimedToken resource implementation."""

from __future__ import annotations

import attrs
import pytest
import pyvider.protocols.tfprotov6.protobuf as pb
from provide.testkit import FoundationTestCase
from pyvider.conversion import marshal, unmarshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers import (
    ApplyResourceChangeHandler,
    PlanResourceChangeHandler,
    ReadResourceHandler,
)
from pyvider.resources.private_state import PrivateState

from pyvider.components.resources.timed_token import (
    TimedTokenPrivateState,
    TimedTokenResource,
)


@attrs.define(frozen=True)
class MockPrivateState(PrivateState):
    """Mock private state class for unit tests"""

    secret_token: str
    internal_id: str
    version: int = 1


class TestTimedTokenResource(FoundationTestCase):
    """Test the fixed TimedToken resource implementation"""

    @pytest.mark.usefixtures("provider_in_hub")
    @pytest.mark.asyncio
    async def test_timed_token_lifecycle(self, encryption_key_env):
        """Test complete lifecycle of TimedToken resource with private state"""
        resource_name = "pyvider_timed_token"
        hub.register("resource", resource_name, TimedTokenResource)

        try:
            schema = TimedTokenResource.get_schema()
            raw_config = {"name": "test-token"}
            config_dv = marshal(raw_config, schema=schema.block)

            # Plan
            plan_request = pb.PlanResourceChange.Request(
                type_name=resource_name, config=config_dv, proposed_new_state=config_dv
            )

            plan_response = await PlanResourceChangeHandler(plan_request, context=None)
            assert not plan_response.diagnostics
            assert plan_response.planned_private

            # Apply
            apply_request = pb.ApplyResourceChange.Request(
                type_name=resource_name,
                config=config_dv,
                planned_state=plan_response.planned_state,
                planned_private=plan_response.planned_private,
            )

            apply_response = await ApplyResourceChangeHandler(apply_request, context=None)
            assert not apply_response.diagnostics
            assert apply_response.private

            final_state = unmarshal(apply_response.new_state, schema=schema.block)
            assert final_state.value["name"].value == "test-token"
            assert final_state.value["id"].value.startswith("timed-token-id-")
            assert final_state.value["token"].value.startswith("token-")
            assert "expires_at" in final_state.value

            # Read
            read_request = pb.ReadResource.Request(
                type_name=resource_name,
                current_state=apply_response.new_state,
                private=apply_response.private,
            )

            read_response = await ReadResourceHandler(read_request, context=None)
            assert not read_response.diagnostics

            read_state = unmarshal(read_response.new_state, schema=schema.block)
            # Verify read state matches apply state
            assert read_state.value["name"].value == final_state.value["name"].value
            assert read_state.value["id"].value == final_state.value["id"].value
            assert read_state.value["token"].value == final_state.value["token"].value

        finally:
            hub.unregister("resource", resource_name)

    def test_timed_token_private_state_structure(self):
        """Test that TimedTokenPrivateState has the correct structure"""
        private_state = TimedTokenPrivateState(token="test-token", expires_at="2025-08-06T10:00:00Z")

        assert private_state.token == "test-token"
        assert private_state.expires_at == "2025-08-06T10:00:00Z"

        # Test serialization
        state_dict = attrs.asdict(private_state)
        assert state_dict == {
            "token": "test-token",
            "expires_at": "2025-08-06T10:00:00Z",
        }

        # Test deserialization
        restored = TimedTokenPrivateState(**state_dict)
        assert restored == private_state


# 🧩🔧🔚
