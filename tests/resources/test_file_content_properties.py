#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from hypothesis import given, strategies as st
import pytest

from pyvider.components.resources.file_content import FileContentResource
from pyvider.cty.exceptions import CtyValidationError

# Get the schema from the resource
schema = FileContentResource.get_schema()
# Get the CtyType for validation from the schema's block
validator = schema.block.to_cty_type()

# Define a Hypothesis strategy for generating valid FileContent configurations
# This strategy generates dictionaries with 'filename' and 'content' keys,
# where the values are text strings.
valid_configs = st.fixed_dictionaries(
    {"filename": st.text(min_size=1), "content": st.text()}
)


@given(config=valid_configs)
def test_schema_validates_any_valid_config(config):
    """
    This property-based test ensures that any valid configuration dictionary
    successfully passes the schema validation without raising an error.
    Hypothesis will generate hundreds of different valid inputs.
    """
    try:
        validator.validate(config)
    except CtyValidationError as e:
        pytest.fail(f"Validation failed for a valid config: {config}. Error: {e}")


# Define a strategy for generating invalid configurations.
# Here, we generate dictionaries that are missing one of the required keys.
invalid_configs = st.one_of(
    st.fixed_dictionaries({"content": st.text()}),
    st.fixed_dictionaries({"filename": st.text()}),
)


@given(config=invalid_configs)
def test_schema_rejects_configs_with_missing_keys(config):
    """
    This property-based test ensures that any configuration missing a
    required key is correctly rejected by the validator.
    """
    with pytest.raises(CtyValidationError, match="Missing required attribute"):
        validator.validate(config)


# Define a strategy for generating configs with wrong data types.
invalid_type_configs = st.fixed_dictionaries(
    {
        "filename": st.integers(),  # filename should be a string
        "content": st.booleans(),  # content should be a string
    }
)


@given(config=invalid_type_configs)
def test_schema_rejects_configs_with_wrong_types(config):
    """
    This property-based test ensures that configurations with incorrect
    data types for attributes are rejected.
    """
    with pytest.raises(CtyValidationError):
        validator.validate(config)


# 🧩🔧🔚
