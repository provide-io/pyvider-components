---
page_title: "Function: lower"
description: |-
  Convert a string to lowercase characters.
---

# lower (Function)

Return the lowercase version of the provided text. Passing `null` keeps the value `null`.

## Example

```terraform
locals {
  username = provider::pyvider::lower("ADMIN@EXAMPLE.COM") # "admin@example.com"
}
```

## Signature

`lower(input_str: string) -> string`

## Parameters

- `input_str` (string, required) — Text to convert. `null` values are returned as `null`.

## Returns

The lowercase string.
