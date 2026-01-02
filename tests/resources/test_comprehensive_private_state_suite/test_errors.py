#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test error conditions and edge cases."""

from __future__ import annotations

from importlib import import_module
import os

import attrs
from provide.testkit import FoundationTestCase  # type: ignore[import-untyped]
from provide.testkit.mocking import patch  # type: ignore[import-untyped]
import pytest

from pyvider.common.encryption import decrypt, encrypt
from pyvider.conversion import marshal
from pyvider.hub import hub
from pyvider.protocols.tfprotov6.handlers import (
    ApplyResourceChangeHandler,
)
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.resources.context import ResourceContext
from pyvider.resources.private_state import PrivateState

TestPrivateStateResource = import_module(
    "test_comprehensive_private_state_suite.test_encryption"
).TestPrivateStateResource


@attrs.define(frozen=True)
class MockPrivateState(PrivateState):
    """Mock private state class for unit tests"""

    secret_token: str
    internal_id: str
    version: int = 1


class TestPrivateStateErrorHandling(FoundationTestCase):
    """Test error conditions and edge cases"""

    @pytest.mark.asyncio
    async def test_missing_encryption_key_fails(self):
        """Test that missing encryption key causes proper failure"""
        # Temporarily remove encryption key
        with patch.dict(os.environ, {}, clear=True):
            # Reset the cached key
            import pyvider.common.encryption

            pyvider.common.encryption._ENCRYPTION_KEY = None

            from provide.foundation.errors import ConfigurationError

            with pytest.raises(
                ConfigurationError,
                match="Private state shared secret not configured",
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
            # Also clear the key cache to force re-derivation with new key
            from pyvider.common.encryption import clear_encryption_cache

            clear_encryption_cache()

            from pyvider.common.encryption import EncryptionError

            with pytest.raises(EncryptionError, match="Decryption failed"):
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


# 🧩🔧🔚
