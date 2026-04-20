# SPDX-FileCopyrightText: Copyright (c) 2026 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Tests for pyvider-components provider implementation."""

import pytest
from pyvider.hub import hub
from pyvider.providers.base import ProviderMetadata

from pyvider.components.capabilities.core import CoreCapability
from pyvider.components.provider import PyviderProvider


class TestPyviderProvider:
    """Tests for PyviderProvider class."""

    def test_provider_initialization(self):
        """Test that provider initializes correctly."""
        provider = PyviderProvider()

        assert provider.metadata is not None
        assert isinstance(provider.metadata, ProviderMetadata)
        assert provider.metadata.name == "pyvider"
        assert provider.metadata.version == "0.1.0"
        assert provider.metadata.protocol_version == "6"

    def test_provider_metadata(self):
        """Test provider metadata configuration."""
        provider = PyviderProvider()

        # Check default capabilities
        assert provider.metadata.capabilities.plan_destroy is True
        assert provider.metadata.capabilities.get_provider_schema_optional is False
        assert provider.metadata.capabilities.move_resource_state is True

    @pytest.mark.asyncio
    async def test_provider_setup_discovers_capabilities(self):
        """Test that setup() auto-discovers capabilities."""
        provider = PyviderProvider()

        # Ensure core capability is registered in hub
        if not hub.get_component("capability", "core"):
            hub.register("capability", "core", CoreCapability)

        await provider.setup()

        # Should have auto-discovered capabilities
        assert "core" in provider.capabilities
        assert provider.capabilities["provider"] is provider

    @pytest.mark.asyncio
    async def test_provider_setup_creates_schema(self):
        """Test that setup() creates provider schema."""
        provider = PyviderProvider()

        # Ensure core capability is registered
        if not hub.get_component("capability", "core"):
            hub.register("capability", "core", CoreCapability)

        await provider.setup()

        # Should have created final schema
        assert provider._final_schema is not None
        assert provider.config_class is not None

    @pytest.mark.asyncio
    async def test_provider_with_multiple_capabilities(self):
        """Test provider setup with multiple capabilities."""
        from pyvider.components.capabilities.lens import LensCapability

        provider = PyviderProvider()

        # Register capabilities
        if not hub.get_component("capability", "core"):
            hub.register("capability", "core", CoreCapability)
        if not hub.get_component("capability", "lens"):
            hub.register("capability", "lens", LensCapability)

        await provider.setup()

        # Should have discovered multiple capabilities
        assert "core" in provider.capabilities
        assert "lens" in provider.capabilities
        assert "provider" in provider.capabilities


class TestCoreCapability:
    """Tests for CoreCapability class."""

    def test_core_capability_initialization(self):
        """Test core capability initializes without config."""
        _capability = CoreCapability(config=None)
        # Should not raise

    def test_core_capability_schema_contribution(self):
        """Test core capability returns schema with pyvider_testmode."""
        schema_contrib = CoreCapability.get_schema_contribution()

        # Core capability provides pyvider_testmode config attribute
        assert isinstance(schema_contrib, dict)
        assert len(schema_contrib) == 1
        assert "pyvider_testmode" in schema_contrib


class TestProviderRegistration:
    """Tests for provider registration via decorator."""

    def test_provider_is_registered(self):
        """Test that PyviderProvider is marked as registered."""
        # Check registration marker
        assert hasattr(PyviderProvider, "_is_registered_provider")
        assert PyviderProvider._is_registered_provider is True

        # Check registered name
        assert hasattr(PyviderProvider, "_registered_name")
        assert PyviderProvider._registered_name == "pyvider"

    def test_core_capability_is_registered(self):
        """Test that CoreCapability is marked as registered."""
        assert hasattr(CoreCapability, "_is_registered_capability")
        assert CoreCapability._is_registered_capability is True

        assert hasattr(CoreCapability, "_registered_name")
        assert CoreCapability._registered_name == "core"
