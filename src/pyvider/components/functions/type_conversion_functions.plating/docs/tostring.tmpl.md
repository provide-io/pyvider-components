---
page_title: "Function: tostring"
description: |-
  Convert values to their string representation.
---

# tostring (Function)

Produce a string representation of any value. Booleans become lowercase `"true"` / `"false"`, and `null` inputs stay `null`.

## Example Usage

{{ example('tostring') }}

## Signature

`tostring(value: any) -> string`

## Parameters

- `value` (any, required) — Value to convert. Returns `null` when this is `null`.

## Returns

The string form of the value, or `null` when the input is `null`.
