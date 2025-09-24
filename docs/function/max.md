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

```terraform
# Basic numeric function examples

# Addition examples
locals {
  simple_add = provider::pyvider::add(5, 3)      # Returns: 8
  float_add = provider::pyvider::add(2.5, 1.5)   # Returns: 4
  mixed_add = provider::pyvider::add(10, 2.3)    # Returns: 12.3
}

# Subtraction examples
locals {
  simple_subtract = provider::pyvider::subtract(10, 4)    # Returns: 6
  float_subtract = provider::pyvider::subtract(5.5, 2.1)  # Returns: 3.4
  negative_result = provider::pyvider::subtract(3, 7)     # Returns: -4
}

# Multiplication examples
locals {
  simple_multiply = provider::pyvider::multiply(4, 3)     # Returns: 12
  float_multiply = provider::pyvider::multiply(2.5, 4)    # Returns: 10
  zero_multiply = provider::pyvider::multiply(5, 0)       # Returns: 0
}

# Division examples
locals {
  simple_divide = provider::pyvider::divide(12, 3)        # Returns: 4
  float_divide = provider::pyvider::divide(10, 3)         # Returns: 3.333...
  precise_divide = provider::pyvider::divide(15, 3)       # Returns: 5
}

# List operations
locals {
  numbers = [10, 5, 8, 2, 15]

  list_sum = provider::pyvider::sum(local.numbers)         # Returns: 40
  list_min = provider::pyvider::min(local.numbers)         # Returns: 2
  list_max = provider::pyvider::max(local.numbers)         # Returns: 15
}

# Rounding examples
locals {
  round_to_int = provider::pyvider::round(3.7, 0)         # Returns: 4
  round_to_decimal = provider::pyvider::round(3.14159, 2) # Returns: 3.14
  round_negative = provider::pyvider::round(-2.6, 0)      # Returns: -3
}

# Output results for verification
output "numeric_examples" {
  value = {
    addition = {
      simple = local.simple_add
      float = local.float_add
      mixed = local.mixed_add
    }
    subtraction = {
      simple = local.simple_subtract
      float = local.float_subtract
      negative = local.negative_result
    }
    multiplication = {
      simple = local.simple_multiply
      float = local.float_multiply
      zero = local.zero_multiply
    }
    division = {
      simple = local.simple_divide
      float = local.float_divide
      precise = local.precise_divide
    }
    list_operations = {
      sum = local.list_sum
      min = local.list_min
      max = local.list_max
    }
    rounding = {
      to_int = local.round_to_int
      to_decimal = local.round_to_decimal
      negative = local.round_negative
    }
  }
}
```

### Capacity Planning



### Performance Analysis



### Resource Scaling



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