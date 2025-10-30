---
page_title: "Function: format_size"
description: |-
  Convert byte counts into human-readable strings.
---

# format_size (Function)

Scale byte values to the nearest unit (B, KB, MB, GB) with an optional precision argument. Helpful for quick summaries in outputs and dashboards.

## Example Usage

{{ example('format_size') }}

## Signature

`format_size(size_bytes: number, options: variadic) -> string`

## Parameters

- `size_bytes` (number, required) — Total bytes to format. Returns `null` when this is `null`.
- `options` (variadic, optional) — First value controls decimal places (default `1`).

## Returns

A human-readable size string such as `"512.0 B"` or `"3.5 GB"`. A `null` input yields `null`.
