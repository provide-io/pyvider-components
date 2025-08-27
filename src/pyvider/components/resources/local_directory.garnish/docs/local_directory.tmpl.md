---
page_title: "Resource: pyvider_local_directory"
description: |-
  Manages a directory on the local filesystem.
---

# pyvider_local_directory (Resource)

The `pyvider_local_directory` resource ensures that a directory exists at a given path with specified permissions. It can create nested parent directories as needed.

**Note:** This resource only manages the directory itself. On deletion (`terraform destroy`), it will only remove the directory if it is empty. It will not recursively delete contents.

## Example Usage

{{ example("example") }}

## Argument Reference

{{ schema() }}
