---
page_title: "Function: min"
description: |-
  Finds the minimum value in a list of numbers with error handling for empty lists
---

# min (Function)

> Finds the smallest numeric value in a list with null-safe handling and empty list validation

The `min` function finds and returns the smallest number from a list of numbers. It requires at least one number in the list and handles null values gracefully.

## When to Use This

- **Threshold calculations**: Find minimum acceptable values
- **Resource optimization**: Find lowest resource usage or cost
- **Performance metrics**: Identify best performance values
- **Capacity planning**: Find minimum requirements
- **Quality assurance**: Identify minimum quality metrics

**Anti-patterns (when NOT to use):**
- Empty lists (will cause an error)
- Single-value comparisons (just use the value directly)
- Non-numeric data (ensure list contains only numbers)

## Quick Start

```terraform
# Simple minimum
locals {
  prices = [19.99, 15.50, 22.00, 12.75]
  lowest_price = provider::pyvider::min(local.prices)  # Returns: 12.75
}

# Resource minimum
variable "cpu_requirements" {
  default = [2, 4, 1, 8]
}

locals {
  min_cpu_needed = provider::pyvider::min(var.cpu_requirements)  # Returns: 1
}
```

## Examples

### Basic Usage

{{ example("basic") }}

### Resource Planning

{{ example("resource_planning") }}

### Performance Metrics

{{ example("performance_metrics") }}

### Cost Optimization

{{ example("cost_optimization") }}

## Signature

`min(numbers: list[number]) -> number`

## Arguments

- **`numbers`** (list[number], required) - A list of numbers to find the minimum from. Must contain at least one number. Returns `null` if the list is `null`. **Raises an error** if the list is empty.

## Return Value

Returns the smallest number from the list. Preserves the original type (integer or float) of the minimum value.
- Returns `null` if the input list is `null`
- **Raises an error** if the list is empty

## Error Handling

```terraform
# This will cause an error
locals {
  # Error: min() requires at least one number
  # bad_result = provider::pyvider::min([])
}

# Safe usage with validation
variable "values" {
  type = list(number)
}

locals {
  minimum = length(var.values) > 0 ? provider::pyvider::min(var.values) : null
}
```

## Related Functions

- [`max`](./max.md) - Find maximum value in a list
- [`sum`](./sum.md) - Calculate sum of all values in a list
