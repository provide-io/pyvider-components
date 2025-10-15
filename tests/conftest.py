#
# tests/conftest.py
#

import os

import pytest

from pyvider.components.capabilities.lens import LensCapability
from pyvider.hub import hub
from pyvider.hub.discovery import ComponentDiscovery
from pyvider.providers.base import BaseProvider, ProviderMetadata


@pytest.fixture(scope="session")
def provider_in_hub():
    provider = BaseProvider(metadata=ProviderMetadata(name="test", version="0.1.0"))
    hub.register("singleton", "provider", provider)
    hub.register("capability", "lens", LensCapability(config=None))
    yield
    hub.unregister("singleton", "provider")
    hub.unregister("capability", "lens")


@pytest.fixture
def encryption_key_env():
    os.environ["PYVIDER_PRIVATE_STATE_SHARED_SECRET"] = (
        "test-secret-key-for-pytest-session"
    )
    yield
    del os.environ["PYVIDER_PRIVATE_STATE_SHARED_SECRET"]


@pytest.fixture(scope="session")
def discovered_components_session():
    discovery = ComponentDiscovery(hub)
    import asyncio

    asyncio.run(discovery.discover_all())


# 🧪⚙️🔧
