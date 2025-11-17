---
page_title: "Function: length"
description: |-
  Return the number of items in a list, map, or string.
---

# length (Function)

Count items in collections or characters in strings. A `null` input returns `null`.

## Example Usage

{{ example('length') }}

## Signature

`length(collection: list | map | string) -> number`

## Parameters

- `collection` (list | map | string, required) — Value to measure. Returns `null` when this is `null`.

## Returns

The length as a number, or `null` when no collection is provided.
