#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from typing import Any
import uuid

import attrs
import msgpack
from provide.testkit import FoundationTestCase
import pytest

from pyvider.common.encryption import decrypt, encrypt
from pyvider.resources.base import BaseResource
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState
from pyvider.schema import PvsSchema, a_str, s_resource

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
    def get_schema(cls) -> PvsSchema:
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
class TestPrivateStateEncryption(FoundationTestCase):
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
        from pyvider.common.encryption import EncryptionError

        with pytest.raises(EncryptionError, match="Ciphertext too short"):
            decrypt(b"invalid-ciphertext-data")

    @pytest.mark.asyncio
    async def test_decryption_too_short_fails(self, encryption_key_env):
        """Test that decrypting data too short to contain a nonce fails"""
        from pyvider.common.encryption import EncryptionError

        with pytest.raises(EncryptionError, match="Ciphertext too short"):
            decrypt(b"short")


# 🧩🔧🔚
