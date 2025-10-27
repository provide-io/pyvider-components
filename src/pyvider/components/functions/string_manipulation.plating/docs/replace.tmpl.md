---
page_title: "Function: replace"
description: |-
  Replace all occurrences of a substring.
---

# replace (Function)

Produce a new string with each match substituted. Empty strings are used when the search or replacement arguments are `null`.

## Example

```terraform
locals {
  sanitized = provider::pyvider::replace(
    "server:REPLACE_HOST",
    "REPLACE_HOST",
    "db.internal"
  )
  # "server:db.internal"
}
```

## Signature

`replace(string: string, search: string, replacement: string) -> string`

## Parameters

- `string` (string, required) — Text to update. Returns `null` when this is `null`.
- `search` (string, required) — Substring to find. Defaults to `""` when `null`.
- `replacement` (string, required) — Text that replaces each occurrence. Defaults to `""` when `null`.

## Returns

The updated string, or `null` when the input string is `null`.
