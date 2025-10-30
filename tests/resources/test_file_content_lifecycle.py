#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import pytest

from pyvider.conversion import marshal, unmarshal
from pyvider.cty import CtyValue
from pyvider.schema import PvsObjectType, a_bool, a_str, s_resource


@pytest.mark.asyncio
async def test_file_content_plan_apply_lifecycle():
    schema = s_resource(
        {
            "filename": a_str(required=True),
            "content": a_str(required=True),
            "exists": a_bool(computed=True),
            "content_hash": a_str(computed=True),
        }
    )

    assert isinstance(schema.block, PvsObjectType)

    validator_type = schema.block.to_cty_type()
    config_val = validator_type.validate(
        {"filename": "/tmp/test.txt", "content": "hello"}
    )

    # THE FIX: Provide the schema to the marshaller.
    config_dv = marshal(config_val, schema=schema.block)
    unmarshaled_val = unmarshal(config_dv, schema=schema.block)

    assert isinstance(unmarshaled_val, CtyValue)
    assert unmarshaled_val["filename"].value == "/tmp/test.txt"


# 🧩🔧🔚
