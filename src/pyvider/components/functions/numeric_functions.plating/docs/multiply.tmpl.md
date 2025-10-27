---
page_title: "Function: multiply"
description: |-
  Multiply two numbers with `null` safety.
---

# multiply (Function)

Return the product of two numeric values. If either argument is `null`, the result is `null`. Whole-number results are returned as integers.

## Example

```terraform
locals {
  area = provider::pyvider::multiply(4, 2.5) # 10
}
```

## Signature

`multiply(a: number, b: number) -> number`

## Parameters

- `a` (number, required) — First factor. Returns `null` when this or `b` is `null`.
- `b` (number, required) — Second factor.

## Returns

The product, or `null` when either input is `null`. Integer results are cast to whole numbers.
