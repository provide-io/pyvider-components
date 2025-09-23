---
page_title: "Function: to_snake_case"
description: |-
  Converts text to snake_case format with intelligent word separation
---

# to_snake_case (Function)

> Converts text to snake_case format by replacing spaces and other separators with underscores

The `to_snake_case` function converts text to snake_case format, which uses lowercase letters with underscores separating words. It intelligently handles various input formats including camelCase, PascalCase, kebab-case, and space-separated text.

## When to Use This

- **Variable naming**: Convert user input to valid Python/Terraform variable names
- **File naming**: Create consistent snake_case filenames from titles
- **Database columns**: Standardize column names in snake_case format
- **API endpoints**: Convert display names to API-friendly snake_case paths
- **Configuration keys**: Normalize configuration keys to snake_case

**Anti-patterns (when NOT to use):**
- When preserving original case is important
- For display text that should remain readable
- When working with external APIs that expect specific casing
- For content that contains special formatting

## Quick Start

```terraform
# Convert display text to snake_case
locals {
  page_title = "User Profile Settings"
  snake_name = provider::pyvider::to_snake_case(local.page_title)  # Returns: "user_profile_settings"
}

# Convert camelCase to snake_case
variable "apiEndpointName" {
  default = "getUserData"
}

locals {
  endpoint_snake = provider::pyvider::to_snake_case(var.apiEndpointName)  # Returns: "get_user_data"
}
```

## Examples

### Basic Usage

{{ example("basic") }}

### Configuration Normalization

{{ example("config_normalization") }}

### API Integration

{{ example("api_integration") }}

## Schema

{{ schema() }}

## Related Functions

- [`to_camel_case`](./to_camel_case.md) - Convert to camelCase format
- [`to_kebab_case`](./to_kebab_case.md) - Convert to kebab-case format
- [`upper`](./upper.md) - Convert to uppercase
- [`lower`](./lower.md) - Convert to lowercase
- [`replace`](./replace.md) - Replace specific text patterns