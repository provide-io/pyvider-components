---
page_title: "Data Source: pyvider_lens_jq"
description: |-
  Transform JSON with jq queries during plan time.
---

# pyvider_lens_jq (Data Source)

Run jq expressions against JSON text or encoded objects, making it easy to reshape API responses before using them in other resources.

## Example

{{ example("basic") }}

## Schema

{{ schema() }}

## Advanced Examples

For more complex use cases, see:
- `examples/comprehensive.tf` - Complex jq queries including filtering, projecting, and data transformations

## Notes

- Provide JSON via `json_input`; use `jsonencode(...)` when starting from Terraform values.
- The `query` field must contain a valid jq program. Results are returned in the `result` attribute.
- Combine with [`pyvider_http_api`](../http_api.md) or file readers to post-process data without leaving Terraform.
