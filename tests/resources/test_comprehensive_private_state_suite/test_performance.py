#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test performance characteristics of private state handling."""

from __future__ import annotations

import attrs
import msgpack
from provide.testkit import FoundationTestCase
import pytest

from pyvider.common.encryption import decrypt, encrypt
from pyvider.resources.private_state import PrivateState


@attrs.define(frozen=True)
class MockPrivateState(PrivateState):
    """Mock private state class for unit tests"""

    secret_token: str
    internal_id: str
    version: int = 1


class TestPrivateStatePerformance(FoundationTestCase):
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


# 🧩🔧🔚
