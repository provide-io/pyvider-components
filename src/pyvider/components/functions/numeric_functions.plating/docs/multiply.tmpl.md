---
page_title: "Function: multiply"
description: |-
  Multiplies two numbers with intelligent integer conversion
---

# multiply (Function)

The `multiply` function multiplies two numbers (integers or floats) and returns the result. It handles null values gracefully and automatically converts floating-point results to integers when they represent whole numbers, ensuring optimal numeric type selection.

Multiplication is fundamental for scaling calculations, resource sizing, and cost projections. The automatic type optimization ensures that results are presented in their most natural form, with whole numbers returned as integers for clarity.

## Capabilities

This function enables you to:

- **Scaling calculations**: Multiply base values by scaling factors for resource sizing
- **Cost projections**: Calculate total costs by multiplying unit prices by quantities
- **Resource allocation**: Determine total resources needed by multiplying per-unit requirements
- **Rate calculations**: Compute totals by multiplying rates by time periods
- **Capacity planning**: Calculate total capacity by multiplying unit capacity by count

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

Returns the product as a number. The return type is automatically optimized:
- If the result is a whole number, returns an integer
- If the result has decimal places, returns a float
- Returns `null` if either input is `null`

## Common Patterns

### Resource Scaling
```terraform
variable "servers_per_zone" {
  default = 3
}

variable "availability_zones" {
  default = 4
}

locals {
  total_servers = provider::pyvider::multiply(var.servers_per_zone, var.availability_zones)  # 12
}
```

### Cost Calculation
```terraform
variable "instance_price" {
  default = 0.15
}

variable "hours_per_month" {
  default = 730
}

locals {
  monthly_cost = provider::pyvider::multiply(var.instance_price, var.hours_per_month)  # 109.5
}
```

## Related Components

- **add** (Function) - Add two numbers together
- **subtract** (Function) - Subtract one number from another
- **divide** (Function) - Divide one number by another
- **sum** (Function) - Calculate the sum of multiple numbers in a list
