---
page_title: "Resource: pyvider_file_content"
description: |-
  Manage the contents of a local file.
---

# pyvider_file_content (Resource)

Write small configuration files with automatic hashing and drift detection. Updates are performed atomically to avoid partially written files.

## Example

{{ example("basic") }}

## Schema

{{ schema() }}

## Advanced Examples

For more complex use cases, see:
- `examples/advanced.tf` - Real-world configuration file generation patterns
- `examples/template.tf` - Template-based file generation
- `examples/lifecycle.tf` - Create, update, and verification workflows

## Notes

- Specify `filename` and `content`; the provider computes `content_hash`, `exists`, and other read-only fields.
- Works well for generated config, secrets wrappers, or other plain-text assets. Consider alternative tooling for large binaries.
- Import existing files with `terraform import pyvider_file_content.example /path/to/file`.
