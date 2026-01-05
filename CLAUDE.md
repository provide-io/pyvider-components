# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`pyvider-components` is a collection of standard components for the Pyvider Framework - a Python-based Terraform provider framework. The project implements Terraform data sources, resources, and functions that can be consumed through a gRPC plugin interface.

## Architecture & Structure

The codebase follows a component-based architecture with three main component types:

1. **Data Sources** (`src/pyvider/components/data_sources/`) - Read-only data providers for Terraform
2. **Resources** (`src/pyvider/components/resources/`) - Manage stateful infrastructure components  
3. **Functions** (`src/pyvider/components/functions/`) - Stateless utility functions for Terraform

Each component includes:
- Python implementation file
- Integration with the Pyvider RPC plugin system

Key architectural patterns:
- Components inherit from base classes in `pyvider-rpcplugin` (e.g., `DataSourceBase`, `ResourceBase`, `FunctionBase`)
- Uses `attrs` for data validation and schema definition
- Implements gRPC-based communication with Terraform
- Capabilities system for advanced features (lens transformations, API interactions)

## Development Environment Setup

```bash
# Set up the development environment (creates virtual env, installs dependencies)
source ./env.sh

# The script will:
# - Install UV package manager if needed
# - Create platform-specific virtual environment in workenv/
# - Install project dependencies and dev tools
# - Configure PYTHONPATH and tool paths
```

## Common Development Commands

### Testing
```bash
# Run all tests
pytest

# Run specific test file
uv run pytest tests/test_tdd_function_semantics.py

# Run with coverage
uv run pytest --cov=pyvider.components --cov-report=term-missing

# Run tests in parallel
uv run pytest -n auto

# Run with verbose output
uv run pytest -v
```

### Code Quality
```bash
# Type checking
uv run pyright
uv run mypy src/

# Linting and formatting
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# Security scanning
bandit -r src/
```

### Building
```bash
# Build the package
uv build

# Install in editable mode
uv add --editable .

# Sync all dependencies
uv sync --all-groups
```

### Working with Examples
```bash
# Most examples are in the examples/ directory
cd examples/integrated_test/

# Initialize Terraform/OpenTofu
tofu init

# Run the example
tofu apply
```

## Important Project Instructions

- **Rebuild flavor helpers before testing/verification** to avoid using inaccurate helpers
- Platform-specific virtual environments are created under `workenv/` with naming pattern `pyvider-components_${OS}_${ARCH}`
- The project requires Python >=3.11

## Testing Strategy

The test suite includes:
- **Unit tests** for individual functions and components
- **Lifecycle tests** for resources (create, read, update, delete operations)
- **End-to-end tests** for complex workflows like encryption
- **TDD-style tests** for function semantics and stdlib functions

When adding new components:
1. Create the component in the appropriate directory
3. Write comprehensive tests covering all operations
4. Ensure the component registers properly with the Pyvider framework

## Component Development Pattern

When implementing new components:

1. **Data Sources**: Inherit from `DataSourceBase`, implement `read()` method
2. **Resources**: Inherit from `ResourceBase`, implement CRUD operations
3. **Functions**: Inherit from `FunctionBase`, implement `call()` method

All components should:
- Use `attrs` classes for schema definition
- Include proper error handling and diagnostics
- Follow existing naming conventions (snake_case for Python, appropriate for Terraform)
- It can use __future__ annotations to use unquoted annotations
