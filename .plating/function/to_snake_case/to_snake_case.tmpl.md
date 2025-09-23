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

## Common Patterns

### Database Column Mapping
```terraform
variable "column_mappings" {
  type = map(string)
  default = {
    "User Name" = "display_name"
    "Email Address" = "email_field"
    "Created At" = "timestamp_field"
  }
}

locals {
  # Convert display names to snake_case column names
  db_columns = {
    for display_name, field_name in var.column_mappings :
    provider::pyvider::to_snake_case(display_name) => field_name
  }
}
```

### File Path Generation
```terraform
variable "document_titles" {
  type = list(string)
  default = [
    "Monthly Report 2024",
    "User Guide v2.1",
    "API Documentation"
  ]
}

locals {
  # Generate snake_case filenames
  file_paths = [
    for title in var.document_titles :
    "/docs/${provider::pyvider::to_snake_case(title)}.md"
  ]
}
```

### Environment Variable Creation
```terraform
variable "service_configs" {
  type = map(object({
    name = string
    value = string
  }))
  default = {
    "Database Host" = { name = "db_host", value = "localhost" }
    "API Key" = { name = "api_key", value = "secret" }
  }
}

locals {
  # Create environment variables with snake_case names
  env_vars = {
    for key, config in var.service_configs :
    provider::pyvider::to_snake_case(key) => config.value
  }
}
```

## Input Format Handling

The function handles various input formats:

| Input Format | Example | Output |
|--------------|---------|--------|
| Space-separated | "User Profile" | "user_profile" |
| camelCase | "userName" | "user_name" |
| PascalCase | "UserProfile" | "user_profile" |
| kebab-case | "user-profile" | "user_profile" |
| Mixed separators | "user_Profile-Name" | "user_profile_name" |

## Error Handling

### Null Input
```terraform
locals {
  # Returns null for null input
  null_result = provider::pyvider::to_snake_case(null)  # Returns: null
}
```

### Empty String
```terraform
locals {
  # Returns empty string for empty input
  empty_result = provider::pyvider::to_snake_case("")  # Returns: ""
}
```

### Special Characters
```terraform
locals {
  # Handles special characters gracefully
  special_chars = provider::pyvider::to_snake_case("User@Name#123")  # Returns: "user_name_123"
}
```

## Best Practices

### 1. Validate Input
```terraform
variable "user_input" {
  type = string
  validation {
    condition     = length(var.user_input) > 0
    error_message = "Input cannot be empty."
  }
}

locals {
  safe_snake_case = provider::pyvider::to_snake_case(var.user_input)
}
```

### 2. Combine with Other Functions
```terraform
locals {
  # Combine with length validation
  input_text = "My Variable Name"
  snake_result = provider::pyvider::to_snake_case(local.input_text)
  is_valid_length = provider::pyvider::length(local.snake_result) <= 50
}
```

### 3. Use for Resource Naming
```terraform
variable "resource_title" {
  type = string
  default = "Production Database Server"
}

resource "pyvider_local_directory" "named_resource" {
  path = "/tmp/${provider::pyvider::to_snake_case(var.resource_title)}"
}
```

## Performance Considerations

- **Lightweight operation**: String conversion is fast with minimal overhead
- **Memory efficient**: No significant memory allocation
- **Caching friendly**: Results are deterministic and can be cached
- **Batch processing**: Efficient for processing multiple strings

## Related Functions

- [`to_camel_case`](./to_camel_case.md) - Convert to camelCase format
- [`to_kebab_case`](./to_kebab_case.md) - Convert to kebab-case format
- [`upper`](./upper.md) - Convert to uppercase
- [`lower`](./lower.md) - Convert to lowercase
- [`replace`](./replace.md) - Replace specific text patterns