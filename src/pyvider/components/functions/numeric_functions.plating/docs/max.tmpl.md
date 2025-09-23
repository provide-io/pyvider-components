---
page_title: "Function: max"
description: |-
  Finds the maximum value in a list of numbers with error handling for empty lists
---

# max (Function)

> Finds the largest numeric value in a list with null-safe handling and empty list validation

The `max` function finds and returns the largest number from a list of numbers. It requires at least one number in the list and handles null values gracefully.

## When to Use This

- **Capacity planning**: Find maximum resource requirements
- **Performance optimization**: Identify peak performance values
- **Scaling decisions**: Determine maximum load or usage
- **Budget planning**: Find highest costs or allocations
- **Quality metrics**: Identify best performance indicators

**Anti-patterns (when NOT to use):**
- Empty lists (will cause an error)
- Single-value comparisons (just use the value directly)
- Non-numeric data (ensure list contains only numbers)

## Quick Start

```terraform
# Simple maximum
locals {
  scores = [85, 92, 78, 96, 88]
  highest_score = provider::pyvider::max(local.scores)  # Returns: 96
}

# Resource maximum
variable "memory_usage_gb" {
  default = [2.5, 8.1, 4.3, 12.7]
}

locals {
  peak_memory = provider::pyvider::max(var.memory_usage_gb)  # Returns: 12.7
}
```

## Examples

### Basic Usage

{{ example("basic") }}

### Capacity Planning

{{ example("capacity_planning") }}

### Performance Analysis

{{ example("performance_analysis") }}

### Resource Scaling

{{ example("resource_scaling") }}

## Signature

`max(numbers: list[number]) -> number`

## Arguments

- **`numbers`** (list[number], required) - A list of numbers to find the maximum from. Must contain at least one number. Returns `null` if the list is `null`. **Raises an error** if the list is empty.

## Return Value

Returns the largest number from the list. Preserves the original type (integer or float) of the maximum value.
- Returns `null` if the input list is `null`
- **Raises an error** if the list is empty

## Error Handling

```terraform
# This will cause an error
locals {
  # Error: max() requires at least one number
  # bad_result = provider::pyvider::max([])
}

# Safe usage with validation
variable "values" {
  type = list(number)
}

locals {
  maximum = length(var.values) > 0 ? provider::pyvider::max(var.values) : null
}
```

## Common Patterns

### Resource Scaling
```terraform
variable "instance_cpu_usage" {
  type = list(number)
  default = [65.2, 82.7, 45.3, 91.8]
}

locals {
  peak_cpu_usage = provider::pyvider::max(var.instance_cpu_usage)
  scale_threshold = 80.0
  needs_scaling = local.peak_cpu_usage > local.scale_threshold
}

resource "pyvider_file_content" "scaling_decision" {
  filename = "/tmp/scaling.txt"
  content  = "Peak CPU: ${local.peak_cpu_usage}%, Scaling needed: ${local.needs_scaling}"
}
```

## Related Functions

- [`min`](./min.md) - Find minimum value in a list
- [`sum`](./sum.md) - Calculate sum of all values in a list
