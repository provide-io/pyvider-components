---
page_title: "Function: max"
description: |-
  Return the largest number in a list.
---

# max (Function)

Find the maximum value from the provided list. A `null` list returns `null`; an empty list raises a `FunctionError`.

## Example

```terraform
locals {
  highest = provider::pyvider::max([3, 7, 2]) # 7
}
```

## Signature

`max(numbers: list[number]) -> number`

## Parameters

- `numbers` (list[number], required) — Values to evaluate. Must contain at least one element. Returns `null` when this is `null`.

## Returns

The maximum number in the list, or `null` when the list is `null`.
