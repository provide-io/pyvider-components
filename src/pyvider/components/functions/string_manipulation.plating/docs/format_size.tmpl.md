---
page_title: "Function: format_size"
description: |-
  Convert byte counts into human-readable strings.
---

# format_size (Function)

Scale byte values to the nearest unit (B, KB, MB, GB) with an optional precision argument. Helpful for quick summaries in outputs and dashboards.

## Example

```terraform
locals {
  default_display = provider::pyvider::format_size(10240)        # "10.0 KB"
  precise_display = provider::pyvider::format_size(123456789, 2) # "117.74 MB"
}
```

## Signature

`format_size(size_bytes: number, options: variadic) -> string`

## Parameters

- `size_bytes` (number, required) — Total bytes to format. Returns `null` when this is `null`.
- `options` (variadic, optional) — First value controls decimal places (default `1`).

## Returns

A human-readable size string such as `"512.0 B"` or `"3.5 GB"`. A `null` input yields `null`.
