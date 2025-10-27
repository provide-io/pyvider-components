---
page_title: "Function: contains"
description: |-
  Check whether a list includes a value.
---

# contains (Function)

Return `true` when the desired element exists in the list. A `null` list returns `null`.

## Example

```terraform
locals {
  enabled = provider::pyvider::contains(["dev", "qa", "prod"], "prod") # true
}
```

## Signature

`contains(list_to_check: list[any], element: any) -> bool`

## Parameters

- `list_to_check` (list[any], required) — List to search. Returns `null` when this is `null`.
- `element` (any, required) — Value to look for. Compared using standard equality.

## Returns

`true` or `false`, or `null` when the input list is `null`.
