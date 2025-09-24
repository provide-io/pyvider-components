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

### Resource Planning



### Performance Metrics



### Cost Optimization



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