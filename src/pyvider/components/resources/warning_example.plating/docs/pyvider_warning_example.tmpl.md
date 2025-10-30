---
page_title: "Resource: pyvider_warning_example"
description: |-
  Showcase warning and deprecation behavior during provider development.
---

# pyvider_warning_example (Resource)

Sample resource that emits Terraform warnings so you can verify messaging, deprecation notices, and config validation in the provider.

## Example

{{ example("basic") }}

## Schema

{{ schema() }}

## Notes

- Use `name` for the modern attribute. Supplying `old_name` keeps compatibility but triggers a deprecation warning.
- `name` and `source_file` are mutually exclusive; at least one of the three inputs must be supplied.
- Provided for education and automated tests, not production workloads.
