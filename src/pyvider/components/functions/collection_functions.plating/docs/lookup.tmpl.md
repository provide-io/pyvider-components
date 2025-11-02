---
page_title: "Function: lookup"
subcategory: "Functions"
description: |-
  Read a value from a map with an optional default.
---

# lookup (Function)

Fetch a key from a map. Provide a default as the third argument to avoid errors when the key is missing.

## Example Usage

{{ example('lookup') }}

## Signature

`lookup(map_to_search: map[string, any], key: string, options: variadic) -> any`

## Parameters

- `map_to_search` (map[string, any], required) — Map to read. Returns `null` when this is `null`.
- `key` (string, required) — Key to retrieve.
- `options` (variadic, optional) — First value acts as the default result.

## Returns

The matching value, the provided default, or `null` when the map itself is `null`.

## Notes

- Without a default, a missing key raises a `FunctionError`.
