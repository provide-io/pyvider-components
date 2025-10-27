---
page_title: "Function: upper"
description: |-
  Convert a string to uppercase characters.
---

# upper (Function)

Return the uppercase version of the provided text. Passing `null` keeps the value `null`.

## Example

```terraform
locals {
  shout = provider::pyvider::upper("hello world") # "HELLO WORLD"
}
```

## Signature

`upper(input_str: string) -> string`

## Parameters

- `input_str` (string, required) — Text to convert. `null` values are returned as `null`.

## Returns

The uppercase string.
