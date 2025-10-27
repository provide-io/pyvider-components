---
page_title: "Data Source: pyvider_file_info"
description: |-
  Inspect metadata about a file or directory.
---

# pyvider_file_info (Data Source)

Read filesystem metadata without managing the underlying file. Useful for conditional logic before creating resources.

## Example

{{ example("basic") }}

## Schema

{{ schema() }}

## Advanced Examples

For more complex use cases, see:
- `examples/advanced.tf` - File validation patterns, conditional resource creation, and metadata access

## Notes

- Returns flags such as `exists`, `is_file`, and `is_dir`, plus size and timestamp fields.
- No files are created or modified; this data source is read-only.
- Combine with resources like `pyvider_file_content` when you need to branch on file presence.
