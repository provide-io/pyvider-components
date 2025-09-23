---
page_title: "Function: subtract"
description: |-
  Subtracts one number from another with intelligent integer conversion
---

# subtract (Function)

> Performs subtraction of two numeric values with null-safe handling and automatic type optimization

The `subtract` function subtracts the second number from the first number and returns the result. It handles null values gracefully and automatically converts floating-point results to integers when they represent whole numbers.

## When to Use This

- **Arithmetic calculations**: Perform basic subtraction in Terraform configurations
- **Countdown operations**: Subtract values from counters or timers
- **Resource calculations**: Compute remaining capacity or quota
- **Configuration math**: Calculate derived configuration values
- **Budget calculations**: Calculate remaining budget or costs

**Anti-patterns (when NOT to use):**
- Complex mathematical operations (use multiple function calls)
- String operations (use string functions)
- List/array operations (use collection functions)
- Boolean logic (use conditional expressions)

## Quick Start

```terraform
# Simple subtraction
locals {
  remaining_quota = provider::pyvider::subtract(100, 25)  # Returns: 75
}

# Subtracting with variables
variable "total_budget" {
  default = 1000
}

variable "spent_amount" {
  default = 250
}

locals {
  remaining_budget = provider::pyvider::subtract(var.total_budget, var.spent_amount)  # Returns: 750
}
```

## Examples

### Basic Usage



### Resource Calculations



### Configuration Math



### Null Handling



## Signature

`subtract(a: number, b: number) -> number`

## Arguments

- **`a`** (number, required) - The number to subtract from (minuend). Can be an integer or float. Returns `null` if this value is `null`.
- **`b`** (number, required) - The number to subtract (subtrahend). Can be an integer or float. Returns `null` if this value is `null`.

## Return Value

Returns the difference of `a - b` as a number. The return type is automatically optimized:
- If the result is a whole number (e.g., `5.0`), returns an integer (`5`)
- If the result has decimal places (e.g., `5.7`), returns a float (`5.7`)
- Returns `null` if either input is `null`

## Related Functions

- [`add`](./add.md) - Add two numbers
- [`multiply`](./multiply.md) - Multiply two numbers
- [`divide`](./divide.md) - Divide two numbers
- [`max`](./max.md) - Find maximum value (useful for ensuring non-negative results)
- [`round`](./round.md) - Round the result to specific precision