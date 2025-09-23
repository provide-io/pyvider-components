---
page_title: "Function: lower"
description: |-
  Converts a string to lowercase with null-safe handling
---

# lower (Function)

> Converts all characters in a string to lowercase with null-safe handling

The `lower` function takes a string and returns a new string with all alphabetic characters converted to lowercase. It handles null values gracefully by returning null when the input is null.

## When to Use This

- **Case normalization**: Standardize text case for comparisons
- **URL/path formatting**: Format paths and URLs consistently
- **Data consistency**: Normalize user input or imported data
- **File naming**: Create consistent lowercase filenames
- **Search operations**: Normalize text for case-insensitive matching

**Anti-patterns (when NOT to use):**
- Preserving original case formatting (use original string)
- Binary data or non-text content
- When case sensitivity is required
- Proper nouns that should maintain capitalization

## Quick Start

```terraform
# Simple case conversion
locals {
  service_name = "USER-SERVICE"
  service_lower = provider::pyvider::lower(local.service_name)  # Returns: "user-service"
}

# File naming
variable "component_name" {
  default = "DataProcessor"
}

locals {
  filename = "${provider::pyvider::lower(var.component_name)}.conf"  # Returns: "dataprocessor.conf"
}
```

## Examples

### Basic Usage

{{ example("basic") }}

### File and Path Naming

{{ example("file_path_naming") }}

### URL Formatting

{{ example("url_formatting") }}

### Case-Insensitive Matching

{{ example("case_insensitive_matching") }}

## Signature

`lower(input_str: string) -> string`

## Arguments

- **`input_str`** (string, required) - The string to convert to lowercase. Returns `null` if this value is `null`.

## Return Value

Returns a new string with all alphabetic characters converted to lowercase:
- Non-alphabetic characters (numbers, symbols, spaces) remain unchanged
- Returns `null` if the input is `null`
- Returns an empty string if the input is an empty string

## Common Patterns

### Configuration Keys
```terraform
variable "config_key" {
  type = string
}

locals {
  normalized_key = provider::pyvider::lower(var.config_key)
}

resource "pyvider_file_content" "config" {
  filename = "/tmp/app.conf"
  content  = "${local.normalized_key}=value"
}
```

### Filename Generation
```terraform
variable "service_name" {
  type = string
}

locals {
  log_filename = "/var/log/${provider::pyvider::lower(var.service_name)}.log"
}
```

## Related Functions

- [`upper`](./upper.md) - Convert string to uppercase
- [`format`](./format.md) - Format strings with placeholders
- [`replace`](./replace.md) - Replace text patterns in strings
