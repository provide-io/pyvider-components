---
page_title: "Function: to_camel_case"
description: |-
  Converts text to camelCase format with optional first letter capitalization
---

# to_camel_case (Function)

> Converts text to camelCase format by removing separators and capitalizing words

The `to_camel_case` function converts text to camelCase format, where the first word is lowercase and subsequent words are capitalized with no separators. It can optionally capitalize the first letter to create PascalCase.

## When to Use This

- **JavaScript variables**: Convert to standard JavaScript naming conventions
- **JSON property names**: Create camelCase keys for JSON objects
- **API field names**: Convert database column names to API-friendly format
- **Function naming**: Generate camelCase function or method names
- **Class properties**: Create property names following camelCase conventions

**Anti-patterns (when NOT to use):**
- Database column names (use snake_case instead)
- File names on case-sensitive systems
- Constants (use UPPER_SNAKE_CASE instead)
- When preserving original formatting is important

## Quick Start

```terraform
# Convert to standard camelCase
locals {
  field_name = "user_profile_data"
  camel_name = provider::pyvider::to_camel_case(local.field_name)  # Returns: "userProfileData"
}

# Convert to PascalCase (first letter capitalized)
locals {
  class_name = "database_connection"
  pascal_name = provider::pyvider::to_camel_case(local.class_name, true)  # Returns: "DatabaseConnection"
}
```

## Examples

### Basic Usage

{{ example("basic") }}

### API Field Mapping

{{ example("api_mapping") }}

### JavaScript Code Generation

{{ example("js_generation") }}

## Schema

{{ schema() }}

## Common Patterns

### Database to API Mapping
```terraform
variable "database_columns" {
  type = list(string)
  default = [
    "user_id",
    "first_name",
    "last_name",
    "email_address",
    "created_at"
  ]
}

locals {
  # Convert to camelCase for API response
  api_fields = {
    for column in var.database_columns :
    column => provider::pyvider::to_camel_case(column)
  }
}

resource "pyvider_file_content" "api_mapping" {
  filename = "/tmp/field_mapping.json"
  content = jsonencode(local.api_fields)
}
```

### JavaScript Object Generation
```terraform
variable "config_settings" {
  type = map(any)
  default = {
    "api_endpoint_url" = "https://api.example.com"
    "max_retry_attempts" = 3
    "timeout_in_seconds" = 30
  }
}

locals {
  # Convert keys to camelCase for JavaScript
  js_config = {
    for key, value in var.config_settings :
    provider::pyvider::to_camel_case(key) => value
  }
}
```

### Class Name Generation
```terraform
variable "service_names" {
  type = list(string)
  default = [
    "user_authentication",
    "email_notification",
    "data_validation"
  ]
}

locals {
  # Generate PascalCase class names
  class_names = [
    for service in var.service_names :
    provider::pyvider::to_camel_case(service, true)
  ]
}
```

## Parameters

### `upper_first` Parameter

Controls first letter capitalization:

| upper_first | Input | Output |
|-------------|-------|--------|
| `false` (default) | "user_name" | "userName" |
| `true` | "user_name" | "UserName" |
| `false` | "api-endpoint" | "apiEndpoint" |
| `true` | "api-endpoint" | "ApiEndpoint" |

## Input Format Handling

The function handles various input formats:

| Input Format | Example | camelCase | PascalCase |
|--------------|---------|-----------|------------|
| snake_case | "user_name" | "userName" | "UserName" |
| kebab-case | "user-name" | "userName" | "UserName" |
| Space-separated | "User Name" | "userName" | "UserName" |
| UPPER_SNAKE | "USER_NAME" | "userName" | "UserName" |
| Mixed | "user_Name-ID" | "userNameId" | "UserNameId" |

## Error Handling

### Null Input
```terraform
locals {
  # Returns null for null input
  null_result = provider::pyvider::to_camel_case(null)  # Returns: null
  null_pascal = provider::pyvider::to_camel_case(null, true)  # Returns: null
}
```

### Empty String
```terraform
locals {
  # Returns empty string for empty input
  empty_result = provider::pyvider::to_camel_case("")  # Returns: ""
}
```

### Special Characters
```terraform
locals {
  # Handles special characters gracefully
  special_chars = provider::pyvider::to_camel_case("user@name#123")  # Returns: "userName123"
}
```

## Best Practices

### 1. Use Appropriate Case Style
```terraform
locals {
  # Use camelCase for variables and properties
  variable_name = provider::pyvider::to_camel_case("user_profile")  # "userProfile"

  # Use PascalCase for classes and types
  class_name = provider::pyvider::to_camel_case("user_profile", true)  # "UserProfile"
}
```

### 2. Validate Input Format
```terraform
variable "field_name" {
  type = string
  validation {
    condition     = can(regex("^[a-zA-Z][a-zA-Z0-9_-]*$", var.field_name))
    error_message = "Field name must start with a letter and contain only letters, numbers, underscores, and hyphens."
  }
}

locals {
  camel_field = provider::pyvider::to_camel_case(var.field_name)
}
```

### 3. Combine with Other String Functions
```terraform
locals {
  input_text = "  USER_PROFILE_DATA  "
  # Clean and convert to camelCase
  cleaned_camel = provider::pyvider::to_camel_case(
    provider::pyvider::lower(
      provider::pyvider::replace(local.input_text, " ", "")
    )
  )
}
```

## JavaScript Integration

### Generate JavaScript Configuration
```terraform
variable "app_config" {
  type = map(any)
  default = {
    "database_host" = "localhost"
    "api_base_url" = "https://api.example.com"
    "cache_timeout_seconds" = 300
  }
}

resource "pyvider_file_content" "js_config" {
  filename = "/tmp/config.js"
  content = join("\n", [
    "const config = {",
    join(",\n", [
      for key, value in var.app_config :
      "  ${provider::pyvider::to_camel_case(key)}: ${jsonencode(value)}"
    ]),
    "};"
  ])
}
```

## Performance Considerations

- **Efficient conversion**: Optimized string processing with minimal allocations
- **Memory conscious**: No significant memory overhead
- **Deterministic results**: Same input always produces same output
- **Batch friendly**: Efficient for processing multiple strings

## Related Functions

- [`to_snake_case`](./to_snake_case.md) - Convert to snake_case format
- [`to_kebab_case`](./to_kebab_case.md) - Convert to kebab-case format
- [`upper`](./upper.md) - Convert to uppercase
- [`lower`](./lower.md) - Convert to lowercase
- [`replace`](./replace.md) - Replace specific text patterns