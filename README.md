# Pyvider Components

This repository provides a standard set of components for the [Pyvider](https://github.com/provide-io/pyvider) framework, a Python-based framework for building Terraform providers.

## Getting Started

To use the `pyvider-components` provider, configure it in your Terraform project:

```terraform
terraform {
  required_providers {
    pyvider = {
      source  = "local/providers/pyvider"
      version = "0.1.0"
    }
  }
}

provider "pyvider" {
  # Provider configuration options go here
}
```

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
