---
page_title: "Function: sum"
description: |-
  Calculates the sum of all numbers in a list with intelligent type conversion
---

# sum (Function)

> Calculates the sum of all numeric values in a list with null-safe handling and automatic type optimization

The `sum` function adds all numbers in a list and returns the total. It handles null values gracefully and automatically converts floating-point results to integers when they represent whole numbers.

## When to Use This

- **Aggregate calculations**: Sum multiple values from lists or collections
- **Total calculations**: Calculate totals for costs, quantities, or metrics
- **Accumulation**: Add up values from dynamic lists
- **Budget summation**: Total multiple budget items
- **Resource totals**: Sum resource allocations or usage

**Anti-patterns (when NOT to use):**
- Empty lists without validation (will return 0)
- Non-numeric data (ensure list contains only numbers)
- Single value addition (use `add` for two values)

## Quick Start

```terraform
# Simple sum
locals {
  numbers = [10, 20, 30, 40]
  total = provider::pyvider::sum(local.numbers)  # Returns: 100
}

# Sum with variables
variable "costs" {
  default = [150.50, 75.25, 200.00]
}

locals {
  total_cost = provider::pyvider::sum(var.costs)  # Returns: 425.75
}
```

## Examples

### Basic Usage

{{ example("basic") }}

### Cost Calculations

{{ example("cost_calculations") }}

### Resource Totals

{{ example("resource_totals") }}

### Dynamic Lists

{{ example("dynamic_lists") }}

## Signature

`sum(numbers: list[number]) -> number`

## Arguments

- **`numbers`** (list[number], required) - A list of numbers to sum. Can contain integers and floats. Returns `null` if the list is `null`. Returns `0` for empty lists.

## Return Value

Returns the sum of all numbers in the list as a number. The return type is automatically optimized:
- If the result is a whole number (e.g., `15.0`), returns an integer (`15`)
- If the result has decimal places (e.g., `15.75`), returns a float (`15.75`)
- Returns `null` if the input list is `null`
- Returns `0` for empty lists

## Common Patterns

### Budget Totaling
```terraform
variable "monthly_costs" {
  type = list(number)
  default = [1200.00, 800.50, 450.25, 300.00]
}

locals {
  total_monthly_budget = provider::pyvider::sum(var.monthly_costs)
}

resource "pyvider_file_content" "budget_summary" {
  filename = "/tmp/budget.txt"
  content  = "Total monthly budget: $${local.total_monthly_budget}"
}
```

### Resource Aggregation
```terraform
variable "server_cpu_cores" {
  type = list(number)
  default = [4, 8, 16, 2]
}

locals {
  total_cpu_capacity = provider::pyvider::sum(var.server_cpu_cores)
}
```

### Dynamic Calculation
```terraform
locals {
  usage_metrics = [
    var.app1_cpu_usage,
    var.app2_cpu_usage,
    var.app3_cpu_usage
  ]
  total_cpu_usage = provider::pyvider::sum(local.usage_metrics)
}
```

## Best Practices

### 1. Validate List Contents
```terraform
variable "values" {
  type = list(number)
  validation {
    condition     = length(var.values) > 0
    error_message = "Values list cannot be empty."
  }
}

locals {
  total = provider::pyvider::sum(var.values)
}
```

### 2. Handle Null Lists
```terraform
locals {
  safe_total = var.optional_values != null ? provider::pyvider::sum(var.optional_values) : 0
}
```

## Related Functions

- [`add`](./add.md) - Add two numbers
- [`max`](./max.md) - Find maximum value in a list
- [`min`](./min.md) - Find minimum value in a list
- [`round`](./round.md) - Round the result to specific precision
