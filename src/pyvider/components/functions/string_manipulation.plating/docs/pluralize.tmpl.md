---
page_title: "Function: pluralize"
description: |-
  Choose a singular or plural word based on a count.
---

# pluralize (Function)

Return the correct singular or plural form for a word. Optionally pass a count and a custom plural.

## Example

```terraform
locals {
  summary = provider::pyvider::pluralize("alert", 3)         # "alerts"
  custom  = provider::pyvider::pluralize("person", 2, "people") # "people"
}
```

## Signature

`pluralize(word: string, options: variadic) -> string`

## Parameters

- `word` (string, required) — Base word to pluralize. Returns `null` when this is `null`.
- `options` (variadic, optional) — First value is the count (default `1`); second value overrides the plural form.

## Returns

The singular form when the count is `1`, otherwise the plural. Returns `null` when `word` is `null`.
