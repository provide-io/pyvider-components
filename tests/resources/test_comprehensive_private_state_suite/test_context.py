#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test the convenience methods added to ResourceContext."""

from __future__ import annotations

import os
import uuid
from typing import Any

import attrs
import msgpack
import pytest
from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch

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


@attrs.define(frozen=True)
class MockPrivateState(PrivateState):
    """Mock private state class for unit tests"""

    secret_token: str
    internal_id: str
    version: int = 1


class TestResourceContextConvenienceMethods(FoundationTestCase):
    """Test the convenience methods added to ResourceContext"""

    @pytest.fixture
    def sample_context(self):
        """Create a ResourceContext with private state"""
        private_state = MockPrivateState(
            secret_token="test-token", internal_id="test-internal-id", version=1
        )
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
        original_state = MockPrivateState(
            secret_token="test", internal_id="test-id", version=1
        )
        context = ResourceContext(private_state=original_state)

        retrieved = context.get_private_state(MockPrivateState)
        assert retrieved is original_state  # Should be the same object


# 🧩🔧🔚
