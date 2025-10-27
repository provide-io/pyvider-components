---
page_title: "Function: add"
description: |-
  Add two numbers with `null` safety.
---

# add (Function)

Return the sum of two numeric values. If either argument is `null`, the result is `null`. Whole-number results are returned as integers.

## Example Usage

{{ example('add') }}

## Signature

`add(a: number, b: number) -> number`

## Parameters

- `a` (number, required) — First addend. Returns `null` when this or `b` is `null`.
- `b` (number, required) — Second addend.

## Returns

The sum, or `null` when either input is `null`. Integer results are cast to whole numbers.
