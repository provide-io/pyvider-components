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

## Related Functions

- [`to_snake_case`](./to_snake_case.md) - Convert to snake_case format
- [`to_kebab_case`](./to_kebab_case.md) - Convert to kebab-case format
- [`upper`](./upper.md) - Convert to uppercase
- [`lower`](./lower.md) - Convert to lowercase
- [`replace`](./replace.md) - Replace specific text patterns