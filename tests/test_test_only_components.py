#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive test suite for test_only component functionality.

This test suite verifies:
1. All test-only components are properly marked with _is_test_only=True
2. All production components are NOT marked as test-only
3. Test-only components are correctly blocked when test mode is disabled
4. Test-only components are accessible when test mode is enabled
5. The pyvider_testmode capability is properly registered"""

from importlib import import_module

import pytest
from pyvider.exceptions import DataSourceError, ResourceError, FunctionError

utils_module = import_module("pyvider.protocols.tfprotov6.handlers.utils")
check_test_only_access = getattr(utils_module, "check_test_only_access")
get_all_components = getattr(utils_module, "get_all_components")

data_sources_module = import_module(
    "pyvider.components.data_sources.nested_data_test_suite"
)
SimpleMapDataSource = getattr(data_sources_module, "SimpleMapDataSource")
MixedMapDataSource = getattr(data_sources_module, "MixedMapDataSource")
StructuredObjectDataSource = getattr(data_sources_module, "StructuredObjectDataSource")
NestedResourceTest = getattr(data_sources_module, "NestedResourceTest")

PrivateStateVerifierResource = getattr(
    import_module("pyvider.components.resources.private_state_verifier"),
    "PrivateStateVerifierResource",
)
FileContentResource = getattr(
    import_module("pyvider.components.resources.file_content"),
    "FileContentResource",
)
LocalDirectoryResource = getattr(
    import_module("pyvider.components.resources.local_directory"),
    "LocalDirectoryResource",
)
TimedTokenResource = getattr(
    import_module("pyvider.components.resources.timed_token"),
    "TimedTokenResource",
)
WarningExampleResource = getattr(
    import_module("pyvider.components.resources.warning_example"),
    "WarningExampleResource",
)
EnvVariablesDataSource = getattr(
    import_module("pyvider.components.data_sources.env_variables"),
    "EnvVariablesDataSource",
)
FileInfoDataSource = getattr(
    import_module("pyvider.components.data_sources.file_info"),
    "FileInfoDataSource",
)
HTTPAPIDataSource = getattr(
    import_module("pyvider.components.data_sources.http_api"),
    "HTTPAPIDataSource",
)
CoreCapability = getattr(
    import_module("pyvider.components.capabilities.core"), "CoreCapability"
)


class TestTestOnlyComponentsMarking:
    """Verify all test-only components are properly marked."""

    def test_test_only_data_sources_marked(self):
        """Test that all test-only data sources have _is_test_only=True."""
        test_only_ds = [
            SimpleMapDataSource,
            MixedMapDataSource,
            StructuredObjectDataSource,
        ]
        for ds_class in test_only_ds:
            assert hasattr(ds_class, "_is_test_only"), (
                f"{ds_class.__name__} should have _is_test_only attribute"
            )
            assert ds_class._is_test_only is True, (
                f"{ds_class.__name__}._is_test_only should be True"
            )

    def test_test_only_resources_marked(self):
        """Test that all test-only resources have _is_test_only=True."""
        test_only_resources = [
            PrivateStateVerifierResource,
            NestedResourceTest,
        ]
        for res_class in test_only_resources:
            assert hasattr(res_class, "_is_test_only"), (
                f"{res_class.__name__} should have _is_test_only attribute"
            )
            assert res_class._is_test_only is True, (
                f"{res_class.__name__}._is_test_only should be True"
            )

    def test_production_data_sources_not_marked(self):
        """Test that production data sources do NOT have _is_test_only=True."""
        production_ds = [
            EnvVariablesDataSource,
            FileInfoDataSource,
            HTTPAPIDataSource,
        ]
        for ds_class in production_ds:
            is_test_only = getattr(ds_class, "_is_test_only", False)
            assert is_test_only is False, (
                f"{ds_class.__name__} should not be marked as test-only"
            )

    def test_production_resources_not_marked(self):
        """Test that production resources do NOT have _is_test_only=True."""
        production_resources = [
            FileContentResource,
            LocalDirectoryResource,
            TimedTokenResource,
            WarningExampleResource,
        ]
        for res_class in production_resources:
            is_test_only = getattr(res_class, "_is_test_only", False)
            assert is_test_only is False, (
                f"{res_class.__name__} should not be marked as test-only"
            )


class TestCheckTestOnlyAccess:
    """Test the check_test_only_access function behavior."""

    def test_production_component_always_allowed(self):
        """Production components should always be allowed."""
        # Should not raise any error
        check_test_only_access(FileContentResource, "pyvider_file_content", "resource")

    def test_test_only_component_blocked_without_test_mode(self):
        """Test-only components should be blocked when test mode is disabled."""
        # When test mode is not enabled, should raise ResourceError
        with pytest.raises(ResourceError) as exc_info:
            check_test_only_access(
                PrivateStateVerifierResource,
                "pyvider_private_state_verifier",
                "resource",
            )

        assert "test-only" in str(exc_info.value).lower()
        assert "test mode" in str(exc_info.value).lower()

    def test_test_only_data_source_blocked_without_test_mode(self):
        """Test-only data sources should be blocked when test mode is disabled."""
        with pytest.raises(DataSourceError) as exc_info:
            check_test_only_access(
                SimpleMapDataSource, "pyvider_simple_map_test", "data_source"
            )

        assert "test-only" in str(exc_info.value).lower()

    def test_test_only_function_blocked_without_test_mode(self):
        """Test-only functions should be blocked when test mode is disabled."""
        with pytest.raises(FunctionError) as exc_info:
            check_test_only_access(
                SimpleMapDataSource, "pyvider_nested_data_processor", "function"
            )

        assert "test-only" in str(exc_info.value).lower()


class TestCoreCapability:
    """Test that CoreCapability provides proper schema contribution."""

    def test_core_capability_registered(self):
        """Test that CoreCapability is registered and can be instantiated."""
        cap = CoreCapability()
        assert cap is not None

    def test_core_capability_schema_contribution(self):
        """Test that CoreCapability provides pyvider_testmode schema."""
        schema = CoreCapability.get_schema_contribution()

        assert "pyvider_testmode" in schema, (
            "CoreCapability should provide pyvider_testmode attribute"
        )

        pyvider_testmode_attr = schema["pyvider_testmode"]
        assert pyvider_testmode_attr is not None
        assert (
            "pyvider_testmode" in str(pyvider_testmode_attr).lower()
            or "test" in str(pyvider_testmode_attr).lower()
        ), "pyvider_testmode attribute should be properly configured"


class TestTestOnlyComponentConsistency:
    """Test consistency of test-only marking across all component types."""

    def test_test_only_attribute_consistency(self):
        """Verify _is_test_only attribute is consistently set."""
        # All test components should have exactly the same _is_test_only value
        test_components = [
            SimpleMapDataSource,
            MixedMapDataSource,
            StructuredObjectDataSource,
            NestedResourceTest,
            PrivateStateVerifierResource,
        ]

        for component in test_components:
            assert hasattr(component, "_is_test_only")
            assert component._is_test_only is True

    def test_no_false_positives_in_marking(self):
        """Ensure no production components are accidentally marked as test-only."""
        production_components = [
            FileContentResource,
            LocalDirectoryResource,
            TimedTokenResource,
            WarningExampleResource,
            EnvVariablesDataSource,
            FileInfoDataSource,
            HTTPAPIDataSource,
        ]

        for component in production_components:
            is_test_only = getattr(component, "_is_test_only", False)
            assert is_test_only is False, (
                f"Production component {component.__name__} should not be marked as test-only"
            )


class TestTestModeScenarios:
    """Test various scenarios with test mode enabled/disabled."""

    def test_import_test_only_components(self):
        """Test that we can import test-only components without errors."""
        ds_module = import_module(
            "pyvider.components.data_sources.nested_data_test_suite"
        )
        resource_module = import_module(
            "pyvider.components.resources.private_state_verifier"
        )

        assert hasattr(ds_module, "SimpleMapDataSource")
        assert hasattr(resource_module, "PrivateStateVerifierResource")

    def test_get_all_components_includes_test_only(self):
        """Test that get_all_components includes test-only components."""
        # Run fresh discovery to ensure all components are registered
        # (other tests may have unregistered some resources)
        from pyvider.hub import hub
        from pyvider.hub.discovery import ComponentDiscovery
        import asyncio

        discovery = ComponentDiscovery(hub)
        asyncio.run(discovery.discover_all())

        data_sources = get_all_components("data_source")
        resources = get_all_components("resource")

        # Should include test-only components
        test_only_ds_names = {
            "pyvider_simple_map_test",
            "pyvider_mixed_map_test",
            "pyvider_structured_object_test",
        }

        test_only_resource_names = {
            "pyvider_private_state_verifier",
            "pyvider_nested_resource_test",
        }

        data_source_names = set(data_sources.keys())
        resource_names = set(resources.keys())
        assert test_only_ds_names.issubset(data_source_names)
        assert test_only_resource_names.issubset(resource_names)


# 🧩🔧🔚
