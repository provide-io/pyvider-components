---
page_title: "Function: split"
description: |-
  Break a string into parts using a delimiter.
---

# split (Function)

Split text into a list of values. A `null` input returns `null`, an empty string yields an empty list, and a `null` delimiter is treated as `""`.

## Example

```terraform
locals {
  hosts = provider::pyvider::split("db1,db2,db3", ",") # ["db1", "db2", "db3"]
}
```

## Signature

`split(string: string, delimiter: string) -> list[string]`

## Parameters

- `string` (string, required) — Text to split. Returns `null` when this is `null`.
- `delimiter` (string, required) — Separator used for splitting. Defaults to `""` when `null`.

## Returns

A list of strings. Empty input text yields `[]`.
