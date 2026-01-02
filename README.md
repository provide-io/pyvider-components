# Pyvider Components

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/uv-package_manager-FF6B35.svg)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/provide-io/pyvider-components/actions/workflows/ci.yml/badge.svg)](https://github.com/provide-io/pyvider-components/actions)

**Example components for the Pyvider Terraform provider framework**

This repository provides a standard set of example components for the [Pyvider](https://github.com/provide-io/pyvider) framework, demonstrating how to build Terraform providers in Python.

## ✨ Key Features

- 📚 **Learning Resources** - Real-world examples of Pyvider components
- 🔧 **Reusable Components** - Data sources, resources, and functions ready to use
- 🧪 **Test Patterns** - Reference implementations for provider testing
- 🏗️ **Build Templates** - Fork and customize for your own providers

## Quick Start

1. Install: `uv add pyvider-components`
2. Read the [Documentation](https://github.com/provide-io/pyvider-components/blob/main/docs/index.md)
3. Explore [Examples](https://github.com/provide-io/pyvider-components/tree/main/examples)

## Getting Started

To use the `pyvider-components` provider, configure it in your Terraform project:

```terraform
terraform {
  required_providers {
    pyvider = {
      source  = "local/providers/pyvider"
      version = ">= 0.0.0"  # For development/learning
      # For specific versions: version = "~> 0.1"
    }
  }
}

provider "pyvider" {
  # Provider configuration options go here
}
```

## Documentation
- [Documentation index](https://github.com/provide-io/pyvider-components/blob/main/docs/index.md)
- [Examples](https://github.com/provide-io/pyvider-components/tree/main/examples)

## Development

To contribute, set up the development environment using `uv`.

```bash
# Create a virtual environment and install all dependencies
uv sync --all-groups

# Activate the environment
source .venv/bin/activate
```

### Testing

Run the test suite with `pytest`.

```bash
pytest
```

## Contributing
See [CONTRIBUTING.md](https://github.com/provide-io/pyvider-components/blob/main/CONTRIBUTING.md) for contribution guidelines.

## License
See [LICENSE](https://github.com/provide-io/pyvider-components/blob/main/LICENSE) for license details.

## What is pyvider-components?

**pyvider-components is a learning and reference library** that demonstrates how to build Terraform provider components using the Pyvider framework. It contains working examples of resources, data sources, and functions that you can:

- 📚 **Learn from** - See real-world examples of Pyvider components
- 🔍 **Reference** - Use as templates for your own providers
- 🧪 **Test with** - Try out Pyvider features without writing code
- 🏗️ **Build on** - Fork and customize for your needs

**Note:** This is primarily an **example/learning library**, not a production provider. For production use, the [terraform-provider-pyvider](#relationship-to-terraform-provider-pyvider) packages these components into a deployable provider.

## Relationship to terraform-provider-pyvider

```
┌─────────────────────────┐
│   pyvider (framework)   │  ← Core framework for building providers
└───────────┬─────────────┘
            │
            ├─────────────────────────────────────┐
            │                                     │
┌───────────▼─────────────┐     ┌───────────────▼──────────────┐
│   pyvider-components    │────▶│  terraform-provider-pyvider  │
│   (example library)     │     │  (POC/example provider)      │
│                         │     │                              │
│  • Learning resources   │     │  • Uses components from ←    │
│  • Reference examples   │     │  • Packaged & tested         │
│  • Component demos      │     │  • POC/Learning tool         │
└─────────────────────────┘     └──────────────────────────────┘
```

**Key Difference:**
- **pyvider-components**: Learn how to build components (this repo)
- **terraform-provider-pyvider**: POC provider for testing and learning ([terraform-provider-pyvider](https://github.com/provide-io/terraform-provider-pyvider))

### When to use pyvider-components

Use this repository when you want to:

✅ Learn how to build Pyvider providers
✅ See working examples of resources, data sources, and functions
✅ Experiment with Pyvider features
✅ Reference implementation patterns
✅ Build your own custom provider

### When to use terraform-provider-pyvider

Use the provider when you want to:

✅ Learn and experiment with Pyvider in Terraform
✅ Test provider functions and resources
✅ Follow a getting started tutorial
✅ Build proof-of-concept configurations

---

## Part of the provide.io Ecosystem

This project is part of a larger ecosystem of tools for Python and Terraform development.

**[View Ecosystem Overview →](https://docs.provide.io/provide-foundation/ecosystem/)**

Understand how provide-foundation, pyvider, flavorpack, and other projects work together.

---

## Components

### Data Sources

-   `pyvider_env_variables`: Provides access to environment variables.
-   `pyvider_file_info`: Provides metadata about a file or directory.
-   `pyvider_http_api`: Makes an HTTP request and returns the response.
-   `pyvider_lens_jq`: Transforms data using a JQ expression.

### Resources

-   `pyvider_file_content`: Manages the content of a file.
-   `pyvider_local_directory`: Manages a directory on the local filesystem.
-   `pyvider_private_state_verifier`: Verifies the private state of a resource (for testing).
-   `pyvider_timed_token`: Manages a short-lived token (for testing).
-   `pyvider_warning_example`: Demonstrates how to return warnings (for testing).

### Functions

A rich set of utility functions are provided for common data manipulations.

-   **Numeric:** `add`, `subtract`, `multiply`, `divide`, `sum`, `min`, `max`, `round`
-   **String:** `upper`, `lower`, `split`, `join`, `replace`, `format`, `truncate`, `format_size`, `pluralize`, `to_snake_case`, `to_kebab_case`, `to_camel_case`
-   **Collection:** `length`, `contains`, `lookup`
-   **Type Conversion:** `tostring`
-   **Transformation:** `lens_jq`

## Examples

### Read Environment Variables

```terraform
data "pyvider_env_variables" "shell" {
  keys = ["SHELL"]
}

output "shell_path" {
  value = data.pyvider_env_variables.shell.values["SHELL"]
}
```

### Manage a File

```terraform
resource "pyvider_file_content" "example" {
  filename = "/tmp/example.txt"
  content  = "This file is managed by Terraform."
}

output "file_hash" {
  value = pyvider_file_content.example.content_hash
}
```

### Use a String Function

```terraform
output "uppercase_example" {
  value = provider::pyvider::upper("hello world")
}
```

Copyright (c) provide.io LLC.
