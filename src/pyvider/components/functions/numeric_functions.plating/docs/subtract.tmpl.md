---
page_title: "Function: subtract"
description: |-
  Subtracts one number from another with intelligent integer conversion
---

# subtract (Function)

The `subtract` function subtracts the second number from the first and returns the result. It handles null values gracefully and automatically converts floating-point results to integers when they represent whole numbers, providing clean and predictable numeric operations.

Like the add function, subtract optimizes result types to ensure that whole numbers are returned as integers rather than floats. This makes configurations more readable and prevents unnecessary decimal notation in outputs and resource calculations.

## Capabilities

This function enables you to:

- **Arithmetic calculations**: Perform basic subtraction in Terraform configurations
- **Counter decrements**: Subtract values from existing counters or totals
- **Resource calculations**: Compute remaining capacity or available resources
- **Delta calculations**: Calculate differences between baseline and current values
- **Budget calculations**: Determine remaining budget or cost differences

## Example Usage

{{ example("example") }}

## Signature

`{{ signature_markdown }}`

## Arguments

{{ arguments_markdown }}

{% if has_variadic %}
## Variadic Arguments

{{ variadic_argument_markdown }}
{% endif %}

## Return Value

Returns the difference as a number. The return type is automatically optimized:
- If the result is a whole number, returns an integer
- If the result has decimal places, returns a float
- Returns `null` if either input is `null`

## Common Patterns

### Remaining Capacity Calculation
```terraform
variable "total_capacity" {
  default = 100
}

variable "current_usage" {
  default = 35
}

locals {
  remaining_capacity = provider::pyvider::subtract(var.total_capacity, var.current_usage)  # 65
}
```

### Budget Remaining
```terraform
variable "budget_allocated" {
  default = 5000.00
}

variable "budget_spent" {
  default = 3250.75
}

locals {
  budget_remaining = provider::pyvider::subtract(var.budget_allocated, var.budget_spent)  # 1749.25
}
```
