---
page_title: "Function: sum"
description: |-
  Sum a list of numbers.
---

# sum (Function)

Add every value in a list. A `null` list returns `null`. Integer totals are returned as whole numbers.

## Example

```terraform
locals {
  total_cost = provider::pyvider::sum([10, 20.5, 5]) # 35.5
}
```

## Signature

`sum(numbers: list[number]) -> number`

## Parameters

- `numbers` (list[number], required) — Values to add. Returns `null` when this is `null`. An empty list yields `0`.

## Returns

The sum of the list, or `null` when the list is `null`.
