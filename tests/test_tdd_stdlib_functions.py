#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


import pytest
from pyvider.exceptions import FunctionError

# Functions to be tested
from pyvider.components.functions.collection_functions import contains, length, lookup
from pyvider.components.functions.string_manipulation import format_str, join
from pyvider.components.functions.type_conversion_functions import tostring


class TestStdlibFunctions:
    """
    TDD: Verifies the contracts for standard library functions.
    """

    # --- collection_functions ---
    def test_length_of_list(self):
        assert length(["a", "b", "c"]) == 3

    def test_length_of_map(self):
        assert length({"a": 1, "b": 2}) == 2

    def test_length_of_string(self):
        assert length("hello") == 5

    def test_length_of_null_is_null(self):
        assert length(None) is None

    def test_contains_in_list_true(self):
        assert contains(["a", "b", "c"], "b") is True

    def test_contains_in_list_false(self):
        assert contains(["a", "b", "c"], "d") is False

    def test_contains_with_null_list_is_null(self):
        assert contains(None, "a") is None

    def test_lookup_success(self):
        assert lookup({"a": "found"}, "a", "default") == "found"

    def test_lookup_fallback_to_default(self):
        assert lookup({"a": "found"}, "b", "default") == "default"

    def test_lookup_raises_error_without_default(self):
        with pytest.raises(FunctionError, match="Invalid key for map lookup"):
            lookup({"a": "found"}, "b")

    def test_lookup_with_null_map_returns_null(self):
        assert lookup(None, "a", "default") is None

    # --- type_conversion_functions ---
    def test_tostring_on_string(self):
        assert tostring("hello") == "hello"

    def test_tostring_on_number(self):
        assert tostring(123) == "123"
        assert tostring(123.45) == "123.45"

    def test_tostring_on_bool(self):
        assert tostring(True) == "true"
        assert tostring(False) == "false"

    def test_tostring_on_null_is_null(self):
        assert tostring(None) is None

    # --- string_manipulation functions (for boolean conversion) ---
    def test_format_with_boolean_uses_lowercase(self):
        """Verifies that format() converts booleans to lowercase 'true'/'false'."""
        result = format_str("The value is {0}", [True])
        assert result == "The value is true"

    def test_join_with_boolean_uses_lowercase(self):
        """Verifies that join() converts booleans to lowercase 'true'/'false'."""
        result = join(", ", ["a", True, 123, False])
        assert result == "a, true, 123, false"

    # --- format: %-style placeholder support (regression for Bug #1) ---
    def test_format_percent_s_placeholders(self):
        """format() should support %s placeholders."""
        result = format_str("Provider: %s v%s", ["pyvider", "0.3.21"])
        assert result == "Provider: pyvider v0.3.21"

    def test_format_percent_s_single_value(self):
        """format() should support a single %s placeholder."""
        result = format_str("Count: %s", [42])
        assert result == "Count: 42"

    def test_format_braces_still_work(self):
        """format() should still support {} placeholders."""
        result = format_str("{} + {} = {}", [1, 2, 3])
        assert result == "1 + 2 = 3"

    def test_format_percent_d_placeholder(self):
        """format() should support %d placeholders."""
        result = format_str("Value: %d", [42])
        assert result == "Value: 42"

    def test_format_null_template_returns_null(self):
        assert format_str(None, ["a"]) is None

    def test_format_empty_values_percent_s(self):
        """format() with %s but no values should raise FunctionError."""
        with pytest.raises(FunctionError):
            format_str("Hello %s", [])


# 🧩🔧🔚
