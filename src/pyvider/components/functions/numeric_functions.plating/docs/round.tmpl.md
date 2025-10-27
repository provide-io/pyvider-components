---
page_title: "Function: round"
description: |-
  Round a number to a chosen precision.
---

# round (Function)

Round numbers to the nearest integer or decimal place. Provide an optional second argument to control precision (defaults to `0`).

## Example

```terraform
locals {
  integer_round = provider::pyvider::round(3.6)      # 4
  precise_round = provider::pyvider::round(3.14159, 2) # 3.14
}
```

## Signature

`round(number: number, options: variadic) -> number`

## Parameters

- `number` (number, required) — Value to round. Returns `null` when this is `null`.
- `options` (variadic, optional) — First value specifies decimal places (default `0`).

## Returns

The rounded number, or `null` when the input is `null`.
