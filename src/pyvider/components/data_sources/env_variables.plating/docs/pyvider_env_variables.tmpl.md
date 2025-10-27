---
page_title: "Data Source: pyvider_env_variables"
description: |-
  Read environment variables for use in Terraform.
---

# pyvider_env_variables (Data Source)

Fetch environment variables by explicit key, prefix, or regex. Optional key/value transformations and `sensitive_keys` help control the output.

## Example

{{ example("basic") }}

## Schema

{{ schema() }}

## Notes

- Provide `keys`, `prefix`, or `regex` to decide which variables are returned.
- Set `case_sensitive = false` to relax matching.
- `key_transform` / `value_transform` accept `"lower"` or `"upper"`.
- Use `sensitive_keys` to mark returned entries as sensitive.
