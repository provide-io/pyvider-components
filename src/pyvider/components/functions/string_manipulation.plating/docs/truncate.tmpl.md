---
page_title: "Function: truncate"
description: |-
  Shorten text to a maximum length with an optional suffix.
---

# truncate (Function)

Trim text to a target length. Provide optional arguments for the limit and suffix; defaults are `100` characters and `"..."`.

## Example

```terraform
locals {
  preview = provider::pyvider::truncate("This is a very long sentence.", 12) # "This is a..."
}
```

## Signature

`truncate(text: string, options: variadic) -> string`

## Parameters

- `text` (string, required) — Text to truncate. Returns `null` when this is `null`.
- `options` (variadic, optional) — First value sets `max_length` (default `100`); second value overrides the suffix (default `"..."`).

## Returns

The truncated string. If the text fits within the limit, it is returned unchanged.
