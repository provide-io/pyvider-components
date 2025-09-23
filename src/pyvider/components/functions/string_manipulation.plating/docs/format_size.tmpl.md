---
page_title: "Function: format_size"
description: |-
  Formats byte values as human-readable file sizes with customizable precision
---

# format_size (Function)

> Converts byte values to human-readable file size strings with automatic unit selection

The `format_size` function formats byte values into human-readable strings using appropriate units (B, KB, MB, GB, TB, PB). It automatically selects the most appropriate unit and allows customizable decimal precision.

## When to Use This

- **File size display**: Show file sizes in user-friendly format
- **Storage reports**: Display storage usage and capacity
- **Bandwidth monitoring**: Format network transfer amounts
- **Memory usage**: Display RAM or cache sizes
- **Progress indicators**: Show download/upload progress

**Anti-patterns (when NOT to use):**
- When exact byte values are needed for calculations
- For non-size numeric values (use appropriate number formatting)
- When binary units (1024-based) are specifically required
- In APIs where raw byte values are expected

## Quick Start

```terraform
# Format file sizes
locals {
  file_sizes = [1024, 1048576, 1073741824]
  formatted_sizes = [
    for size in local.file_sizes :
    provider::pyvider::format_size(size)
  ]
  # Returns: ["1.0 KB", "1.0 MB", "1.0 GB"]
}

# Custom precision
locals {
  large_file = 1234567890
  precise_size = provider::pyvider::format_size(local.large_file, 2)  # Returns: "1.15 GB"
  rounded_size = provider::pyvider::format_size(local.large_file, 0)  # Returns: "1 GB"
}
```

## Examples

### Basic Usage

{{ example("basic") }}

### Storage Analysis

{{ example("storage_analysis") }}

### File Management

{{ example("file_management") }}

## Schema

{{ schema() }}

## Related Functions

- [`tostring`](./tostring.md) - Convert values to string format
- [`round`](./round.md) - Round numeric values
- [`add`](./add.md) - Add numeric values for totals
- [`multiply`](./multiply.md) - Calculate size multiplications
- [`divide`](./divide.md) - Calculate size divisions