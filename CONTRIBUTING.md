# Contributing to Pyvider Components

Thank you for your interest in contributing! This guide provides the necessary information to get you started with development.

## Project Architecture

The codebase is structured into three main component types:

1.  **Data Sources**: Located in `src/pyvider/components/data_sources/`. These are for read-only data access.
2.  **Resources**: Located in `src/pyvider/components/resources/`. These manage stateful infrastructure.
3.  **Functions**: Located in `src/pyvider/components/functions/`. These are stateless utility functions.

Components inherit from base classes in the `pyvider-rpcplugin` library and use `attrs` for defining configuration and state schemas.

## Development Environment Setup

This project uses `uv` for package and environment management.

1.  **Install `uv`**:
    If you don't have it, install it with:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Create and Sync the Environment**:
    This command creates a virtual environment (`.venv`) and installs all required dependencies from `uv.lock`.
    ```bash
    uv sync --all-groups
    ```

3.  **Activate the Environment**:
    ```bash
    source .venv/bin/activate
    ```

## Common Development Commands

All commands should be run from the project root with the virtual environment activated.

### Testing

We use `pytest` for testing.

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src/pyvider/components --cov-report=term-missing
```

### Code Quality

We use `ruff` for linting/formatting and `mypy` for type checking.

```bash
# Check for linting errors and format code
ruff check . --fix
ruff format .

# Run the type checker
mypy src/
```

## Adding a New Component

1.  **Create the Python File**: Add your new component to the appropriate directory under `src/pyvider/components/`.
2.  **Implement the Component**:
    -   Inherit from the correct base class (`BaseDataSource`, `BaseResource`, or `BaseFunction`).
    -   Use the `@register_*` decorator.
    -   Define `attrs` classes for configuration and state.
    -   Implement the required methods (`read`, `_create`, `call`, etc.).
3.  **Add Documentation and Examples**:
    -   Create a `.plating/` directory alongside your component file (e.g., `src/pyvider/components/resources/my_resource.plating/`).
    -   Add a `docs/my_resource.tmpl.md` documentation template.
    -   Add a `basic.tf` example in `examples/`. **This example should be the simplest possible demonstration of the component's core feature.**
    -   Optionally, add an `advanced.tf` for more complex use cases.
4.  **Write Tests**: Add comprehensive tests for your component in the `tests/` directory, mirroring the source structure.
