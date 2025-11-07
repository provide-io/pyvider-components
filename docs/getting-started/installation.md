# Installation

This guide covers installing **pyvider-components** for both library usage and development.

## Prerequisites

--8<-- ".provide/foundry/docs/_partials/python-requirements.md"

--8<-- ".provide/foundry/docs/_partials/uv-installation.md"

--8<-- ".provide/foundry/docs/_partials/python-version-setup.md"

## Installation Methods

### As a Library Dependency

If you're building a Terraform provider with Pyvider, add `pyvider-components` to your project:

```bash
# Add to your project dependencies
uv add pyvider-components

# Or specify a version
uv add "pyvider-components>=0.1.0"
```

**In your `pyproject.toml`:**
```toml
[project]
dependencies = [
    "pyvider-components>=0.1.0",
]
```

### For Development

Clone the repository and set up the development environment:

```bash
# Clone the repository
git clone https://github.com/provide-io/pyvider-components.git
cd pyvider-components

# Set up development environment using the provided script
source ./env.sh
```

The `env.sh` script will:
- Install UV package manager if needed
- Create a platform-specific virtual environment in `workenv/`
- Install project dependencies and dev tools
- Configure PYTHONPATH and tool paths

!!! note "Platform-Specific Environments"
    The development environment uses platform-specific naming: `workenv/pyvider-components_${OS}_${ARCH}`. This allows parallel development across different platforms.

--8<-- ".provide/foundry/docs/_partials/virtual-env-setup.md"

--8<-- ".provide/foundry/docs/_partials/platform-specific-macos.md"

## Verifying Installation

### Basic Verification

--8<-- ".provide/foundry/docs/_partials/verification-commands.md"

### Component-Specific Verification

**1. Verify Component Registration:**
```bash
# List all registered components
pyvider components list

# Check specific component types
python -c "from pyvider.components import resources; print(dir(resources))"
```

**2. Test Component Imports:**
```bash
# Verify all component modules can be imported
python -c "
from pyvider.components.data_sources import *
from pyvider.components.resources import *
from pyvider.components.functions import *
print('✅ All components imported successfully')
"
```

**3. Run Integration Tests:**
```bash
# Test component lifecycle operations
uv run pytest tests/test_lifecycle_*.py -v

# Test function semantics
uv run pytest tests/test_tdd_function_semantics.py -v
```

## Development Workflow

--8<-- ".provide/foundry/docs/_partials/testing-setup.md"

--8<-- ".provide/foundry/docs/_partials/code-quality-setup.md"

### Building the Package

```bash
# Build distribution packages
uv build

# Install in editable mode for development
uv pip install -e .

# Sync all dependencies including dev groups
uv sync --all-groups
```

### Working with Examples

The repository includes Terraform examples for testing components:

```bash
cd examples/integrated_test/

# Initialize Terraform/OpenTofu
tofu init

# Run the example
tofu plan
tofu apply
```

## Component Development

When developing new components for the library:

**1. Component Types:**
- **Data Sources** (`src/pyvider/components/data_sources/`) - Read-only data providers
- **Resources** (`src/pyvider/components/resources/`) - Stateful infrastructure management
- **Functions** (`src/pyvider/components/functions/`) - Stateless utility functions

**2. Development Pattern:**
```python
# Data source example
from pyvider.rpcplugin import DataSourceBase

class MyDataSource(DataSourceBase):
    async def read(self, config):
        # Implementation
        return result

# Register with decorator
@register_data_source("my_data_source")
class MyDataSource(DataSourceBase):
    pass
```

**3. Testing Requirements:**
- Unit tests for component logic
- Lifecycle tests for resources (CRUD operations)
- Integration tests with Terraform/OpenTofu

!!! tip "Rebuild Flavor Helpers"
    Before testing or verification, rebuild flavor helpers to ensure accuracy:
    ```bash
    # Rebuild will be done automatically by test suite
    uv run pytest
    ```

## Troubleshooting

--8<-- ".provide/foundry/docs/_partials/troubleshooting-common.md"

### Component-Specific Issues

**Components Not Registering:**

If components aren't being discovered:
```bash
# Check PYTHONPATH includes src directory
echo $PYTHONPATH

# Verify package structure
python -c "import pyvider.components; print(pyvider.components.__file__)"

# Check for registration decorators in component files
grep -r "@register_" src/pyvider/components/
```

**Import Errors with attrs:**

The project uses `attrs` for data validation:
```bash
# Ensure attrs is installed
uv add attrs

# Verify attrs version compatibility
python -c "import attr; print(attr.__version__)"
```

**Platform-Specific Build Issues:**

If you encounter issues with the `workenv/` setup:
```bash
# Remove existing environment
rm -rf workenv/

# Re-run setup script
source ./env.sh

# Verify platform detection
python -c "import platform; print(f'{platform.system()}_{platform.machine()}')"
```

## Next Steps

Now that you have pyvider-components installed:

1. **[Understand the Framework](../guides/orientation.md)** - Learn core Pyvider concepts
2. **[Build Your Own Provider](../guides/build-your-own.md)** - Create a custom provider
3. **[Explore Components](../index.md)** - Browse available resources, data sources, and functions

## Additional Resources

- [Pyvider Framework Documentation](https://foundry.provide.io/pyvider/)
- [Pyvider RPC Plugin Documentation](https://foundry.provide.io/pyvider-rpcplugin/)
- [GitHub Repository](https://github.com/provide-io/pyvider-components)
