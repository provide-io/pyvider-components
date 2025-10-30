# 
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

import json

import pytest

from pyvider.components.capabilities.lens import LensCapability
from pyvider.components.data_sources.lens_jq import (
    LensJqConfig,
    LensJqDataSource,
    LensJqState,
)
from pyvider.resources.context import ResourceContext


@pytest.mark.usefixtures("provider_in_hub")
@pytest.mark.usefixtures("provider_in_hub")
async def test_lens_jq_data_source_with_problematic_input():
    problematic_json_input = json.dumps([{"message": "hello from list"}])
    query = ".[0].message"
    config = LensJqConfig(json_input=problematic_json_input, query=query)

    # Create a live capability instance for injection
    lens_cap = LensCapability(config=None)
    ctx = ResourceContext(config=config, capabilities={"lens": lens_cap})

    data_source = LensJqDataSource()
    state = await data_source.read(ctx, lens=lens_cap)

    assert isinstance(state, LensJqState)
    assert state.result == "hello from list"

# 🧩🔧🔚
