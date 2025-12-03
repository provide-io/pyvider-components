#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from unittest.mock import MagicMock

import attrs
import pytest
from pyvider.exceptions import DataSourceError, FunctionError
from pyvider.resources.context import ResourceContext

from pyvider.components.capabilities.lens import LensCapability
from pyvider.components.data_sources.lens_jq import LensJqDataSource
from pyvider.components.functions.lens_jq import lens_jq


@attrs.define
class MockLensProviderConfig:
    lens_enabled: bool = True


@pytest.mark.usefixtures("provider_in_hub")
class TestTddLensCapabilityRequirement:
    @pytest.fixture
    def capability_factory(self):
        def _factory(enabled: bool):
            mock_config = MockLensProviderConfig(lens_enabled=enabled)
            return LensCapability(config=mock_config)

        return _factory

    @pytest.mark.asyncio
    async def test_data_source_fails_when_capability_is_disabled(self, capability_factory):
        disabled_lens_cap = capability_factory(enabled=False)
        data_source = LensJqDataSource()
        ctx = ResourceContext(config=data_source.config_class("{}", "."))
        with pytest.raises(DataSourceError, match="The 'lens' capability is disabled"):
            await data_source.read(ctx, lens=disabled_lens_cap)

    @pytest.mark.asyncio
    async def test_data_source_succeeds_and_calls_service_when_enabled(self, capability_factory):
        enabled_lens_cap = capability_factory(enabled=True)
        enabled_lens_cap.jq = MagicMock()
        data_source = LensJqDataSource()
        ctx = ResourceContext(config=data_source.config_class('{"a":1}', ".a"))
        await data_source.read(ctx, lens=enabled_lens_cap)
        enabled_lens_cap.jq.assert_called_once_with(".a", {"a": 1})

    def test_function_fails_when_capability_is_disabled(self, capability_factory):
        disabled_lens_cap = capability_factory(enabled=False)
        with pytest.raises(FunctionError, match="The 'lens' capability is disabled"):
            lens_jq(input_data={}, query=".", lens=disabled_lens_cap)

    def test_function_succeeds_and_calls_service_when_enabled(self, capability_factory):
        enabled_lens_cap = capability_factory(enabled=True)
        enabled_lens_cap.jq = MagicMock()
        lens_jq(input_data={"a": 1}, query=".a", lens=enabled_lens_cap)
        enabled_lens_cap.jq.assert_called_once_with(".a", {"a": 1})


# 🧩🔧🔚
