---
page_title: "Data Source: pyvider_env_variables"
description: |-
  Reads environment variables for use in Terraform configurations.
---

# pyvider_env_variables (Data Source)

Fetches environment variables by key, prefix, or regex. This allows you to inject external configuration into your Terraform plans.

## Example Usage

{{ example("basic") }}

## Schema

{{ schema() }}

## Advanced Examples

For more complex use cases, see:
- `examples/advanced.tf` - Basic filtering and transformations
- `examples/filtering.tf` - Regex patterns and credential filtering
- `examples/multi_environment.tf` - Dev/staging/prod configuration patterns
- `examples/comprehensive.tf` - Complete feature showcase including sensitive handling and exclusions

## Notes

- You must provide one of `keys`, `prefix`, or `regex` to specify which variables to read.
- Use `sensitive_keys` to mark specific variables as sensitive, preventing them from being displayed in logs or outputs.
