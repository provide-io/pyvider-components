# Test-Only Component System

This document describes the test-only component system for pyvider-components.

## Overview

The test-only system allows components to be marked as for-testing-only, which means they will be filtered out in production environments unless explicitly enabled via `provider_testmode = true`.

## How It Works

### 1. Component Marking

Components are marked as test-only using the `test_only=True` parameter in their decorator:

```python
@register_resource("pyvider_example_test", test_only=True)
class ExampleTestResource(BaseResource):
    # ...
```

This automatically sets the `_is_test_only` class attribute to `True`.

### 2. Runtime Filtering

At runtime, the system:

1. **Checks provider configuration**: Reads `provider_testmode` from the provider config
2. **Sets test mode flag**: The `ProviderContext` is initialized with `test_mode_enabled` based on this config
3. **Filters components**: Uses `get_filtered_components()` which returns only production components when test mode is disabled
4. **Blocks access**: The `check_test_only_access()` function raises an error if a test-only component is accessed without test mode enabled

### 3. Provider Configuration

The `CoreCapability` in `src/pyvider/components/capabilities/core.py` provides the `provider_testmode` attribute to the provider schema:

```hcl
terraform {
  required_providers {
    pyvider = {
      source = "provide.io/pyvider"
    }
  }
}

provider "pyvider" {
  provider_testmode = true  # Enable test-only components
}
```

## Test-Only Components

### Data Sources
- `pyvider_simple_map_test` - Tests simple string map handling
- `pyvider_mixed_map_test` - Tests mixed-type map handling
- `pyvider_structured_object_test` - Tests well-defined nested object structures

### Resources
- `pyvider_private_state_verifier` - Tests private state encryption/decryption
- `pyvider_nested_resource_test` - Tests nested configuration data

### Functions
- `pyvider_nested_data_processor` - Test function for processing nested JSON data

## Implementation Details

### Decorator Integration

The `@register_resource`, `@register_data_source`, and `@register_function` decorators from the pyvider framework automatically:

1. Accept a `test_only` parameter (defaults to `False`)
2. Set `cls._is_test_only = test_only` on the component class
3. Pass the `test_only` flag to the hub's registration system

### Access Control

The `check_test_only_access()` function in `pyvider/protocols/tfprotov6/handlers/utils.py`:

1. Checks if a component has `_is_test_only = True`
2. Retrieves the provider context from the hub
3. Checks if `test_mode_enabled` is true
4. Raises an appropriate error (DataSourceError, ResourceError, or FunctionError) if access is denied

### Component Filtering

The `get_filtered_components()` function:

1. Retrieves all components from the hub
2. Checks if test mode is enabled
3. Filters out test-only components if test mode is disabled
4. Returns the appropriate component set

## Testing

A comprehensive test suite is provided in `tests/test_test_only_components.py` that verifies:

- ✅ All test-only components are properly marked
- ✅ All production components are not marked as test-only
- ✅ Test-only components are blocked without test mode
- ✅ Production components are always accessible
- ✅ The CoreCapability provides the required schema
- ✅ Test-only components can be imported successfully

Run tests with:
```bash
pytest tests/test_test_only_components.py -v
```

## Best Practices

1. **Mark test components consistently**: Use `test_only=True` for all test-related components
2. **Clear naming**: Include "test" in component names for clarity
3. **Documentation**: Add docstrings explaining the component's test purpose
4. **Cleanup**: Organize test components in dedicated test files
5. **Error messages**: Leverage the built-in error messages that guide users to enable test mode

## Examples

### Creating a Test-Only Resource

```python
from pyvider.resources.base import BaseResource
from pyvider.hub import register_resource

@register_resource("pyvider_my_test_resource", test_only=True)
class MyTestResource(BaseResource):
    """A test-only resource for testing specific functionality."""
    # Implementation...
```

### Creating a Test-Only Data Source

```python
from pyvider.data_sources.base import BaseDataSource
from pyvider.data_sources.decorators import register_data_source

@register_data_source("pyvider_my_test_data", test_only=True)
class MyTestDataSource(BaseDataSource):
    """A test-only data source for testing specific functionality."""
    # Implementation...
```

### Using Test-Only Components in Terraform

```hcl
provider "pyvider" {
  provider_testmode = true
}

resource "pyvider_my_test_resource" "example" {
  # Configuration...
}

data "pyvider_my_test_data" "example" {
  # Configuration...
}
```

## Troubleshooting

### Error: "Component is test-only and requires test mode"

**Solution**: Add `provider_testmode = true` to your provider configuration

### Test components not appearing in schema

**Solution**: Verify:
1. `provider_testmode = true` is set in provider config
2. Component is registered with `test_only=True`
3. Component class has `_is_test_only = True` attribute

### Cannot find component in autocomplete

**Solution**: This is expected if test mode is not enabled. Either:
1. Enable test mode in your provider config
2. Use a production component instead

---

For more information about the pyvider framework, see the [Pyvider Documentation](https://github.com/provide-io/pyvider).
