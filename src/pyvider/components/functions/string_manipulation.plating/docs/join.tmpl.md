page_title: "Function: join"
description: |-
  Join list elements into a single string.
---

# join (Function)

Combine list values with a delimiter. Non-string items are coerced with `tostring`, and a `null` delimiter behaves like an empty string.

## Example

{{ example("basic") }}

## Signature

`join(delimiter: string, strings: list[any]) -> string`

## Parameters

- `delimiter` (string, required) — Separator placed between items; defaults to `""` when `null`.
- `strings` (list[any], required) — Values to concatenate; each value is converted to a string. Returns `null` when the list itself is `null`.

## Returns

A single string containing all items. An empty list produces `""`.
