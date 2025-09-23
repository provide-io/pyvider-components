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

## Common Patterns

### Storage Usage Report
```terraform
variable "storage_volumes" {
  type = list(object({
    name = string
    used_bytes = number
    total_bytes = number
  }))
  default = [
    {
      name = "system"
      used_bytes = 21474836480
      total_bytes = 107374182400
    },
    {
      name = "data"
      used_bytes = 549755813888
      total_bytes = 1099511627776
    }
  ]
}

locals {
  storage_report = [
    for volume in var.storage_volumes : {
      name = volume.name
      used = provider::pyvider::format_size(volume.used_bytes, 1)
      total = provider::pyvider::format_size(volume.total_bytes, 1)
      used_percent = (volume.used_bytes * 100) / volume.total_bytes
    }
  ]
}

resource "pyvider_file_content" "storage_report" {
  filename = "/tmp/storage_usage.txt"
  content = join("\n", concat(
    ["=== Storage Usage Report ===", ""],
    [
      for vol in local.storage_report :
      "${vol.name}: ${vol.used} / ${vol.total} (${format("%.1f", vol.used_percent)}%)"
    ]
  ))
}
```

### File Inventory
```terraform
variable "file_inventory" {
  type = list(object({
    path = string
    size_bytes = number
    type = string
  }))
  default = [
    { path = "/app/logs/system.log", size_bytes = 52428800, type = "log" },
    { path = "/app/data/users.db", size_bytes = 2147483648, type = "database" },
    { path = "/app/backup.tar.gz", size_bytes = 5368709120, type = "archive" }
  ]
}

locals {
  # Group files by type and calculate totals
  files_by_type = {
    for file in var.file_inventory :
    file.type => file.size_bytes...
  }

  type_summaries = {
    for type, sizes in local.files_by_type :
    type => {
      count = length(sizes)
      total_bytes = sum(sizes)
      total_formatted = provider::pyvider::format_size(sum(sizes), 2)
      avg_bytes = sum(sizes) / length(sizes)
      avg_formatted = provider::pyvider::format_size(sum(sizes) / length(sizes), 2)
    }
  }
}
```

### Bandwidth Monitoring
```terraform
variable "network_usage" {
  type = object({
    upload_bytes = number
    download_bytes = number
    period_hours = number
  })
  default = {
    upload_bytes = 1073741824
    download_bytes = 5368709120
    period_hours = 24
  }
}

locals {
  network_stats = {
    upload_total = provider::pyvider::format_size(var.network_usage.upload_bytes, 2)
    download_total = provider::pyvider::format_size(var.network_usage.download_bytes, 2)
    total_transfer = provider::pyvider::format_size(
      var.network_usage.upload_bytes + var.network_usage.download_bytes, 2
    )

    # Calculate rates
    upload_rate_bytes = var.network_usage.upload_bytes / (var.network_usage.period_hours * 3600)
    download_rate_bytes = var.network_usage.download_bytes / (var.network_usage.period_hours * 3600)

    upload_rate = "${provider::pyvider::format_size(local.upload_rate_bytes, 1)}/s"
    download_rate = "${provider::pyvider::format_size(local.download_rate_bytes, 1)}/s"
  }
}
```

## Precision Control

The `precision` parameter controls decimal places:

| Input Bytes | Precision | Output |
|-------------|-----------|--------|
| 1536 | 0 | "2 KB" |
| 1536 | 1 | "1.5 KB" |
| 1536 | 2 | "1.50 KB" |
| 1536 | 3 | "1.500 KB" |

## Unit Conversion Chart

| Range | Unit | Example |
|-------|------|---------|
| 0 - 1023 | B | "512 B" |
| 1024 - 1048575 | KB | "1.5 KB" |
| 1048576 - 1073741823 | MB | "2.3 MB" |
| 1073741824 - 1099511627775 | GB | "4.7 GB" |
| 1099511627776 - 1125899906842623 | TB | "1.2 TB" |
| 1125899906842624+ | PB | "3.4 PB" |

## Error Handling

### Null Input
```terraform
locals {
  # Returns null for null input
  null_result = provider::pyvider::format_size(null)  # Returns: null
}
```

### Negative Values
```terraform
locals {
  # Handles negative values gracefully
  negative_size = provider::pyvider::format_size(-1024)  # Returns: "-1.0 KB"
}
```

### Zero Values
```terraform
locals {
  # Returns "0 B" for zero
  zero_size = provider::pyvider::format_size(0)  # Returns: "0 B"
}
```

### Large Values
```terraform
locals {
  # Handles very large numbers
  huge_size = provider::pyvider::format_size(1152921504606846976, 1)  # Returns: "1.0 EB"
}
```

## Best Practices

### 1. Consistent Precision
```terraform
variable "precision_level" {
  type = number
  default = 1
  validation {
    condition     = var.precision_level >= 0 && var.precision_level <= 3
    error_message = "Precision must be between 0 and 3."
  }
}

locals {
  # Use consistent precision throughout
  sizes = [1024, 1048576, 1073741824]
  formatted = [
    for size in local.sizes :
    provider::pyvider::format_size(size, var.precision_level)
  ]
}
```

### 2. Input Validation
```terraform
variable "file_size" {
  type = number
  validation {
    condition     = var.file_size >= 0
    error_message = "File size cannot be negative."
  }
}

locals {
  safe_format = provider::pyvider::format_size(var.file_size, 2)
}
```

### 3. Performance Monitoring
```terraform
variable "performance_metrics" {
  type = map(number)
  default = {
    memory_used = 2147483648
    disk_io = 1073741824
    network_throughput = 134217728
  }
}

resource "pyvider_file_content" "performance_report" {
  filename = "/tmp/performance_metrics.txt"
  content = join("\n", [
    "=== Performance Metrics ===",
    "Memory Used: ${provider::pyvider::format_size(var.performance_metrics.memory_used, 1)}",
    "Disk I/O: ${provider::pyvider::format_size(var.performance_metrics.disk_io, 1)}",
    "Network Throughput: ${provider::pyvider::format_size(var.performance_metrics.network_throughput, 1)}"
  ])
}
```

## Display Formatting

### Table Generation
```terraform
variable "disk_usage" {
  type = list(object({
    path = string
    size_bytes = number
  }))
  default = [
    { path = "/var/log", size_bytes = 536870912 },
    { path = "/tmp", size_bytes = 1073741824 },
    { path = "/home", size_bytes = 21474836480 }
  ]
}

resource "pyvider_file_content" "disk_usage_table" {
  filename = "/tmp/disk_usage.csv"
  content = join("\n", concat(
    ["Path,Size (Bytes),Size (Formatted)"],
    [
      for item in var.disk_usage :
      "${item.path},${item.size_bytes},${provider::pyvider::format_size(item.size_bytes, 2)}"
    ]
  ))
}
```

## Performance Considerations

- **Fast formatting**: Efficient calculation with minimal overhead
- **Memory efficient**: No significant memory allocation
- **Locale independent**: Consistent output regardless of system locale
- **Precision control**: Configurable output precision

## Related Functions

- [`tostring`](./tostring.md) - Convert values to string format
- [`round`](./round.md) - Round numeric values
- [`add`](./add.md) - Add numeric values for totals
- [`multiply`](./multiply.md) - Calculate size multiplications
- [`divide`](./divide.md) - Calculate size divisions