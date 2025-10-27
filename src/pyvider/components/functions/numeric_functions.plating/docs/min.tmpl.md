---
page_title: "Function: min"
description: |-
  Return the smallest number in a list.
---

# min (Function)

Find the minimum value from the provided list. A `null` list returns `null`; an empty list raises a `FunctionError`.

## Example

```terraform
locals {
  lowest = provider::pyvider::min([3, 7, 2]) # 2
}
```

## Signature

`min(numbers: list[number]) -> number`

## Parameters

- `numbers` (list[number], required) — Values to evaluate. Must contain at least one element. Returns `null` when this is `null`.

## Returns

The minimum number in the list, or `null` when the list is `null`.
