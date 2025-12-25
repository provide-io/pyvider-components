#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import json
from pathlib import Path
from typing import Any

import pytest
import pyvider.protocols.tfprotov6.protobuf as pb
from pyvider.conversion import cty_to_native, marshal, unmarshal
from pyvider.cty import CtyDynamic, CtyList, CtyString, CtyValue
from pyvider.protocols.tfprotov6.handlers import CallFunctionHandler

from pyvider.components.capabilities.lens import LensCapability
from pyvider.components.functions.lens_jq import lens_jq as lens_jq_function

TF_DATA_PATH = Path(__file__).parent.parent.parent / "fixtures" / "advanced_jq_test"


@pytest.fixture(scope="module")
def personnel_data() -> dict[str, Any]:
    records_path = TF_DATA_PATH / "personnel_records.json"
    return json.loads(records_path.read_text())


@pytest.mark.usefixtures("provider_in_hub")
class TestJqWireProtocol:
    def test_lens_jq_function_returns_native_value(self, personnel_data: dict):
        query = "[.records[].name]"
        result = lens_jq_function(personnel_data, query, lens=LensCapability(config=None))

        assert isinstance(result, list)
        assert result == ["Dr. Evelyn Reed", "Dr. Jian Chen", "Maria Rosa"]

    @pytest.mark.usefixtures("discovered_components_session")
    async def test_full_lifecycle_with_corrected_function(self, personnel_data: dict):
        raw_args = [personnel_data, "[.records[].name]"]
        marshalled_arg1 = marshal(raw_args[0], schema=CtyDynamic())
        marshalled_arg2 = marshal(raw_args[1], schema=CtyString())
        request = pb.CallFunction.Request(name="lens_jq", arguments=[marshalled_arg1, marshalled_arg2])
        response = await CallFunctionHandler(request, context=None)
        assert not response.error.text, f"Handler returned an error: {response.error.text}"
        result_cty = unmarshal(response.result, schema=CtyDynamic())
        assert isinstance(result_cty, CtyValue)
        assert isinstance(result_cty.type, CtyDynamic)
        assert isinstance(result_cty.value.type, CtyList)
        assert result_cty.value.type.element_type.equal(CtyString())
        native_result = cty_to_native(result_cty)
        assert native_result == ["Dr. Evelyn Reed", "Dr. Jian Chen", "Maria Rosa"]


# 🧩🔧🔚
