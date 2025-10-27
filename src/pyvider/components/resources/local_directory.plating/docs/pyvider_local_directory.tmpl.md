---
page_title: "Resource: pyvider_local_directory"
description: |-
  Ensure a directory exists with optional permissions.
---

# pyvider_local_directory (Resource)

Create or verify a directory on the local filesystem and optionally manage its permissions.

## Example

{{ example("basic") }}

## Schema

{{ schema() }}

## Notes

- Set `path` to the directory to manage. Existing directories are adopted into state.
- Use the optional `permissions` attribute with the `0o###` octal format for mode management.
- Computed fields expose `exists`, `file_count`, and effective permission data for downstream logic.
- Import existing directories with `terraform import pyvider_local_directory.example /path/to/dir`.
