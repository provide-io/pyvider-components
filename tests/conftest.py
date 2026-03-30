#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import os
import sys

# On Windows, prevent UnicodeEncodeError from emoji/box-drawing characters in
# provide.foundation's structured logger.  colorama wraps sys.stdout with an
# AnsiToWin32 proxy whose .wrapped attribute is the real cp1252 TextIOWrapper.
# That reference is saved in structlog's PrintLogger._file before pytest
# replaces sys.stdout with its capture buffer.  Reconfiguring the underlying
# streams (sys.__stdout__ / sys.__stderr__) to UTF-8 fixes all write paths.
if sys.platform == "win32":
    for _real in (sys.__stdout__, sys.__stderr__, sys.stdout, sys.stderr):
        if _real is None:
            continue
        if hasattr(_real, "reconfigure"):
            try:
                _real.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
            except Exception:
                pass
        for _attr in ("wrapped", "stream"):
            _inner = getattr(_real, _attr, None)
            if _inner is not None and hasattr(_inner, "reconfigure"):
                try:
                    _inner.reconfigure(encoding="utf-8", errors="replace")
                except Exception:
                    pass

import pytest

from pyvider.components.capabilities.lens import LensCapability
from pyvider.hub import hub
from pyvider.hub.discovery import ComponentDiscovery
from pyvider.providers.base import BaseProvider, ProviderMetadata

# Register pytest plugins for test fixtures
pytest_plugins = [
    "pyvider.testmode.fixtures",
]


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
    os.environ["PYVIDER_PRIVATE_STATE_SHARED_SECRET"] = "test-secret-key-for-pytest-session"
    yield
    del os.environ["PYVIDER_PRIVATE_STATE_SHARED_SECRET"]


@pytest.fixture(scope="session")
def discovered_components_session():
    discovery = ComponentDiscovery(hub)
    import asyncio

    asyncio.run(discovery.discover_all())


# 🧩🔧🔚
