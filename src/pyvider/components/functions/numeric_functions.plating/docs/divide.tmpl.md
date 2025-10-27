---
page_title: "Function: divide"
description: |-
  Divide one number by another with error handling.
---

# divide (Function)

Return the quotient of two numeric values. If either argument is `null`, the result is `null`. Whole-number results are returned as integers.

## Example

```terraform
locals {
  average = provider::pyvider::divide(21, 4) # 5.25
}
```

## Signature

`divide(a: number, b: number) -> number`

## Parameters

- `a` (number, required) — Dividend. Returns `null` when this or `b` is `null`.
- `b` (number, required) — Divisor. Must not be zero.

## Returns

The quotient, or `null` when either input is `null`.

## Notes

- Division by zero raises a `FunctionError`.
