---
page_title: "Function: subtract"
description: |-
  Subtract one number from another with `null` safety.
---

# subtract (Function)

Return the difference between two numeric values. If either argument is `null`, the result is `null`. Whole-number results are returned as integers.

## Example Usage

{{ example('subtract') }}

## Signature

`subtract(a: number, b: number) -> number`

## Parameters

- `a` (number, required) — Minuend. Returns `null` when this or `b` is `null`.
- `b` (number, required) — Subtrahend.

## Returns

The difference, or `null` when either input is `null`. Integer results are cast to whole numbers.
