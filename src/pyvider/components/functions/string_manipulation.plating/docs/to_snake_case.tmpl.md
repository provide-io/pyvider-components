---
page_title: "Function: to_snake_case"
description: |-
  Convert text to snake_case.
---

# to_snake_case (Function)

Transform input text to lowercase words separated by underscores.

## Example

```terraform
locals {
  identifier = provider::pyvider::to_snake_case("Display Name") # "display_name"
}
```

## Signature

`to_snake_case(text: string) -> string`

## Parameters

- `text` (string, required) — Text to transform. Returns `null` for `null` input.

## Returns

The snake_case string.
