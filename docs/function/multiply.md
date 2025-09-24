---
page_title: "Function: multiply"
description: |-
  Multiplies two numbers with intelligent integer conversion and null-safe handling
---

# multiply (Function)

> Performs multiplication of two numeric values with null-safe handling and automatic type optimization

The `multiply` function multiplies two numbers (integers or floats) and returns the result. It handles null values gracefully and automatically converts floating-point results to integers when they represent whole numbers.

## When to Use This

- **Scaling calculations**: Scale values by multipliers or factors
- **Resource sizing**: Calculate total capacity based on unit size
- **Area calculations**: Compute areas, volumes, or dimensions
- **Cost calculations**: Calculate total costs based on unit prices
- **Percentage calculations**: Apply percentage multipliers

**Anti-patterns (when NOT to use):**
- Complex mathematical operations (use multiple function calls)
- String repetition (use appropriate string functions)
- List/array operations (use collection functions)
- Boolean logic (use conditional expressions)

## Quick Start

```terraform
# Simple multiplication
locals {
  total_storage = provider::pyvider::multiply(10, 5)  # Returns: 50
}

# Scaling with variables
variable "instances" {
  default = 4
}

variable "cpu_per_instance" {
  default = 2
}

locals {
  total_cpu = provider::pyvider::multiply(var.instances, var.cpu_per_instance)  # Returns: 8
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

### Resource Scaling



### Cost Calculations



### Null Handling



## Signature

`multiply(a: number, b: number) -> number`

## Arguments

- **`a`** (number, required) - The first number to multiply. Can be an integer or float. Returns `null` if this value is `null`.
- **`b`** (number, required) - The second number to multiply. Can be an integer or float. Returns `null` if this value is `null`.

## Return Value

Returns the product of `a` and `b` as a number. The return type is automatically optimized:
- If the result is a whole number (e.g., `6.0`), returns an integer (`6`)
- If the result has decimal places (e.g., `6.75`), returns a float (`6.75`)
- Returns `null` if either input is `null`

## Common Patterns

### Resource Capacity
```terraform
variable "nodes" {
  type    = number
  default = 3
}

variable "cores_per_node" {
  type    = number
  default = 8
}

locals {
  total_cores = provider::pyvider::multiply(var.nodes, var.cores_per_node)
}

resource "pyvider_file_content" "capacity_report" {
  filename = "/tmp/capacity.txt"
  content  = "Total CPU cores: ${local.total_cores}"
}
```

### Cost Estimation
```terraform
variable "unit_price" {
  type = number
}

variable "quantity" {
  type = number
}

locals {
  total_cost = provider::pyvider::multiply(var.unit_price, var.quantity)
}
```

## Related Functions

- [`add`](./add.md) - Add two numbers
- [`subtract`](./subtract.md) - Subtract two numbers
- [`divide`](./divide.md) - Divide two numbers
- [`round`](./round.md) - Round the result to specific precision