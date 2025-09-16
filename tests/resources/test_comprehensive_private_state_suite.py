#
# tests/resources/test_comprehensive_private_state_suite.py
#

"""
Comprehensive Private State Test Suite

Tests all aspects of Pyvider's private state functionality including:
- Encryption/decryption roundtrip tests
- Full resource lifecycle with private state
- ResourceContext convenience methods
- Error handling and edge cases
- TimedToken resource validation
- Cross-resource compatibility
"""

import os
from typing import Any
from unittest.mock import patch
import uuid

import attrs
import msgpack
import pytest

from pyvider.common.encryption import decrypt, encrypt
from pyvider.components.resources.private_state_verifier import (
    PrivateStateVerifierResource,
)
from pyvider.components.resources.timed_token import (
    TimedTokenPrivateState,
    TimedTokenResource,
)
from pyvider.conversion import marshal, unmarshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers import (
    ApplyResourceChangeHandler,
    PlanResourceChangeHandler,
    ReadResourceHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import a_str, s_resource


# Test Fixtures and Mock Resources
@attrs.define(frozen=True)
class MockPrivateState(PrivateState):
    """Mock private state class for unit tests"""

    secret_token: str
    internal_id: str
    version: int = 1


@attrs.define(frozen=True)
class MockResourceState:
    """Mock resource state class"""

    name: str | None = None
    public_id: str | None = None


@attrs.define(frozen=True)
class MockResourceConfig:
    """Mock resource config class"""

    name: str


class TestPrivateStateResource(BaseResource["test_private_state", MockResourceState, MockResourceConfig]):
    """Test resource that uses private state"""

    config_class = MockResourceConfig
    state_class = MockResourceState
    private_state_class = MockPrivateState

    @classmethod
    def get_schema(cls):
        return s_resource(
            {
                "name": a_str(required=True),
                "public_id": a_str(computed=True),
            }
        )

    async def _validate_config(self, config: MockResourceConfig) -> list[str]:
        return []

    async def _create(
        self, ctx: ResourceContext, base_plan: dict[str, Any]
    ) -> tuple[dict[str, Any], MockPrivateState]:
        base_plan["public_id"] = f"public-{ctx.config.name}"
        private_state = MockPrivateState(
            secret_token=f"secret-{uuid.uuid4()}",
            internal_id=f"internal-{uuid.uuid4()}",
            version=1,
        )
        return base_plan, private_state

    async def _create_apply(self, ctx: ResourceContext) -> tuple[MockResourceState, MockPrivateState]:
        final_state = MockResourceState(name=ctx.config.name, public_id=f"public-{ctx.config.name}")
        # Keep the private state for future reads
        return final_state, ctx.private_state

    async def read(self, ctx: ResourceContext) -> MockResourceState | None:
        if ctx.has_private_state():
            # Use convenience methods to access private state
            ctx.get_private_state(MockPrivateState)
            return MockResourceState(
                name=ctx.state.name if ctx.state else None,
                public_id=ctx.state.public_id if ctx.state else None,
            )
        return ctx.state

    async def _delete_apply(self, ctx: ResourceContext) -> None:
        pass


# Unit Tests for Encryption/Decryption
class TestPrivateStateEncryption:
    """Test the core encryption functionality"""

    @pytest.fixture
    def sample_private_state(self):
        return MockPrivateState(
            secret_token="super-secret-token-123",
            internal_id="internal-abc-def-456",
            version=42,
        )

    @pytest.mark.asyncio
    async def test_encryption_decryption_roundtrip(self, encryption_key_env, sample_private_state):
        """Test that private state can be encrypted and decrypted correctly"""
        # Serialize to msgpack
        serialized = msgpack.packb(attrs.asdict(sample_private_state), use_bin_type=True)

        # Encrypt
        encrypted_data = encrypt(serialized)
        assert encrypted_data != serialized
        assert len(encrypted_data) > len(serialized)  # Should be longer due to nonce + MAC

        # Decrypt
        decrypted_data = decrypt(encrypted_data)
        assert decrypted_data == serialized

        # Deserialize back to object
        deserialized_dict = msgpack.unpackb(decrypted_data, raw=False)
        restored_state = MockPrivateState(**deserialized_dict)

        assert restored_state == sample_private_state

    @pytest.mark.asyncio
    async def test_encryption_produces_different_ciphertext(self, encryption_key_env, sample_private_state):
        """Test that encryption produces different ciphertext each time (due to random nonce)"""
        serialized = msgpack.packb(attrs.asdict(sample_private_state), use_bin_type=True)

        encrypted1 = encrypt(serialized)
        encrypted2 = encrypt(serialized)

        # Should be different due to random nonce
        assert encrypted1 != encrypted2

        # But should decrypt to the same plaintext
        assert decrypt(encrypted1) == decrypt(encrypted2)

    @pytest.mark.asyncio
    async def test_empty_data_encryption(self, encryption_key_env):
        """Test encryption of empty data"""
        assert encrypt(b"") == b""
        assert decrypt(b"") == b""

    @pytest.mark.asyncio
    async def test_decryption_invalid_data_fails(self, encryption_key_env):
        """Test that decrypting invalid data raises an error"""
        with pytest.raises(ValueError, match="Private state decryption failed"):
            decrypt(b"invalid-ciphertext-data")

    @pytest.mark.asyncio
    async def test_decryption_too_short_fails(self, encryption_key_env):
        """Test that decrypting data too short to contain a nonce fails"""
        with pytest.raises(ValueError, match="Invalid ciphertext: too short"):
            decrypt(b"short")


# Unit Tests for ResourceContext Convenience Methods
class TestResourceContextConvenienceMethods:
    """Test the convenience methods added to ResourceContext"""

    @pytest.fixture
    def sample_context(self):
        """Create a ResourceContext with private state"""
        private_state = MockPrivateState(secret_token="test-token", internal_id="test-internal-id", version=1)
        return ResourceContext(private_state=private_state)

    @pytest.fixture
    def empty_context(self):
        """Create a ResourceContext without private state"""
        return ResourceContext()

    def test_has_private_state_returns_true_when_present(self, sample_context):
        """Test has_private_state returns True when private state is present"""
        assert sample_context.has_private_state() is True

    def test_has_private_state_returns_false_when_absent(self, empty_context):
        """Test has_private_state returns False when private state is absent"""
        assert empty_context.has_private_state() is False

    def test_get_private_state_returns_correct_type(self, sample_context):
        """Test get_private_state returns the correct typed instance"""
        private_data = sample_context.get_private_state(MockPrivateState)

        assert private_data is not None
        assert isinstance(private_data, MockPrivateState)
        assert private_data.secret_token == "test-token"
        assert private_data.internal_id == "test-internal-id"
        assert private_data.version == 1

    def test_get_private_state_returns_none_when_absent(self, empty_context):
        """Test get_private_state returns None when no private state exists"""
        private_data = empty_context.get_private_state(MockPrivateState)
        assert private_data is None

    def test_get_private_state_same_type_passthrough(self):
        """Test get_private_state passes through when already correct type"""
        original_state = MockPrivateState(secret_token="test", internal_id="test-id", version=1)
        context = ResourceContext(private_state=original_state)

        retrieved = context.get_private_state(MockPrivateState)
        assert retrieved is original_state  # Should be the same object


# Integration Tests for Full Resource Lifecycle
class TestPrivateStateResourceLifecycle:
    """Test complete resource lifecycle with private state"""

    @pytest.mark.usefixtures("provider_in_hub")
    @pytest.mark.asyncio
    async def test_complete_resource_lifecycle_with_private_state(self, encryption_key_env):
        """Test full CRUD lifecycle of a resource with private state"""
        resource_name = "test_private_state"
        hub.register("resource", resource_name, TestPrivateStateResource)

        try:
            schema = TestPrivateStateResource.get_schema()

            # Plan Phase
            raw_config = {"name": "test-resource"}
            config_dv = marshal(raw_config, schema=schema.block)

            plan_request = pb.PlanResourceChange.Request(
                type_name=resource_name, config=config_dv, proposed_new_state=config_dv
            )

            plan_response = await PlanResourceChangeHandler(plan_request, context=None)
            assert not plan_response.diagnostics, f"Plan failed: {plan_response.diagnostics}"
            assert plan_response.planned_private, "No private state returned from plan"

            # Apply Phase
            apply_request = pb.ApplyResourceChange.Request(
                type_name=resource_name,
                config=config_dv,
                planned_state=plan_response.planned_state,
                planned_private=plan_response.planned_private,
            )

            apply_response = await ApplyResourceChangeHandler(apply_request, context=None)
            assert not apply_response.diagnostics, f"Apply failed: {apply_response.diagnostics}"
            assert apply_response.private, "No private state returned from apply"

            final_state = unmarshal(apply_response.new_state, schema=schema.block)
            assert final_state.value["name"].value == "test-resource"
            assert final_state.value["public_id"].value == "public-test-resource"

            # Read Phase
            read_request = pb.ReadResource.Request(
                type_name=resource_name,
                current_state=apply_response.new_state,
                private=apply_response.private,
            )

            read_response = await ReadResourceHandler(read_request, context=None)
            assert not read_response.diagnostics, f"Read failed: {read_response.diagnostics}"

            read_state = unmarshal(read_response.new_state, schema=schema.block)
            assert read_state.value["name"].value == "test-resource"
            assert read_state.value["public_id"].value == "public-test-resource"

        finally:
            hub.unregister("resource", resource_name)

    @pytest.mark.usefixtures("provider_in_hub")
    @pytest.mark.asyncio
    async def test_private_state_verifier_resource_works(self, encryption_key_env):
        """Test that the existing private state verifier resource still works"""
        resource_name = "pyvider_private_state_verifier"
        hub.register("resource", resource_name, PrivateStateVerifierResource)

        try:
            schema = PrivateStateVerifierResource.get_schema()
            raw_config = {"input_value": "test-verification"}
            config_dv = marshal(raw_config, schema=schema.block)

            plan_request = pb.PlanResourceChange.Request(
                type_name=resource_name, config=config_dv, proposed_new_state=config_dv
            )

            plan_response = await PlanResourceChangeHandler(plan_request, context=None)
            assert not plan_response.diagnostics
            assert plan_response.planned_private

            apply_request = pb.ApplyResourceChange.Request(
                type_name=resource_name,
                config=config_dv,
                planned_state=plan_response.planned_state,
                planned_private=plan_response.planned_private,
            )

            apply_response = await ApplyResourceChangeHandler(apply_request, context=None)
            assert not apply_response.diagnostics

            final_state = unmarshal(apply_response.new_state, schema=schema.block)
            assert final_state.value["input_value"].value == "test-verification"
            assert final_state.value["decrypted_token"].value == "SECRET_FOR_TEST-VERIFICATION"

        finally:
            hub.unregister("resource", resource_name)


# Tests for TimedToken Resource
class TestTimedTokenResource:
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


# Error Handling and Edge Cases
class TestPrivateStateErrorHandling:
    """Test error conditions and edge cases"""

    @pytest.mark.asyncio
    async def test_missing_encryption_key_fails(self):
        """Test that missing encryption key causes proper failure"""
        # Temporarily remove encryption key
        with patch.dict(os.environ, {}, clear=True):
            # Reset the cached key
            import pyvider.common.encryption

            pyvider.common.encryption._ENCRYPTION_KEY = None

            from pyvider.exceptions import FrameworkConfigurationError

            with pytest.raises(
                FrameworkConfigurationError,
                match="Private state shared secret not found",
            ):
                encrypt(b"test-data")

    @pytest.mark.asyncio
    async def test_changed_encryption_key_fails_decryption(self, encryption_key_env):
        """Test that changing encryption key breaks decryption of existing data"""
        # Encrypt with one key
        test_data = b"sensitive-data"
        encrypted = encrypt(test_data)

        # Change the key
        with patch.dict(os.environ, {"PYVIDER_PRIVATE_STATE_SHARED_SECRET": "different-key"}):
            # Reset cached key to force reload
            import pyvider.common.encryption

            pyvider.common.encryption._ENCRYPTION_KEY = None

            with pytest.raises(ValueError, match="Private state decryption failed"):
                decrypt(encrypted)

    @pytest.mark.usefixtures("provider_in_hub")
    @pytest.mark.asyncio
    async def test_corrupted_private_state_fails_gracefully(self, encryption_key_env):
        """Test that corrupted private state in apply phase fails gracefully"""
        resource_name = "test_private_state_error"
        hub.register("resource", resource_name, TestPrivateStateResource)

        try:
            schema = TestPrivateStateResource.get_schema()
            config_dv = marshal({"name": "test"}, schema=schema.block)

            # Create a corrupted private state (not valid encrypted data)
            corrupted_private = b"this-is-not-valid-encrypted-data"

            apply_request = pb.ApplyResourceChange.Request(
                type_name=resource_name,
                config=config_dv,
                planned_state=config_dv,
                planned_private=corrupted_private,
            )

            apply_response = await ApplyResourceChangeHandler(apply_request, context=None)
            assert apply_response.diagnostics, "Expected diagnostics for corrupted private state"
            assert len(apply_response.diagnostics) > 0
            assert "Failed to deserialize private state" in apply_response.diagnostics[0].detail

        finally:
            hub.unregister("resource", resource_name)

    def test_resource_context_convenience_methods_with_none(self):
        """Test ResourceContext convenience methods handle None gracefully"""
        context = ResourceContext(private_state=None)

        assert not context.has_private_state()
        assert context.get_private_state(MockPrivateState) is None


# Performance and Compatibility Tests
class TestPrivateStatePerformance:
    """Test performance characteristics of private state handling"""

    @pytest.mark.asyncio
    async def test_large_private_state_encryption(self, encryption_key_env):
        """Test that large private state objects can be encrypted efficiently"""
        # Create a large private state object
        large_data = {
            "large_field": "x" * 10000,  # 10KB string
            "many_fields": {f"field_{i}": f"value_{i}" for i in range(1000)},
        }

        serialized = msgpack.packb(large_data, use_bin_type=True)
        encrypted = encrypt(serialized)
        decrypted = decrypt(encrypted)
        restored = msgpack.unpackb(decrypted, raw=False)

        assert restored == large_data

    @pytest.mark.asyncio
    async def test_multiple_encryption_operations(self, encryption_key_env):
        """Test multiple encryption operations work consistently"""
        test_states = [MockPrivateState(f"token-{i}", f"id-{i}", i) for i in range(100)]

        # Encrypt all states
        encrypted_states = []
        for state in test_states:
            serialized = msgpack.packb(attrs.asdict(state), use_bin_type=True)
            encrypted = encrypt(serialized)
            encrypted_states.append(encrypted)

        # Decrypt and verify all states
        for i, encrypted in enumerate(encrypted_states):
            decrypted = decrypt(encrypted)
            restored_dict = msgpack.unpackb(decrypted, raw=False)
            restored_state = MockPrivateState(**restored_dict)
            assert restored_state == test_states[i]


# 🧪🔒🎯
