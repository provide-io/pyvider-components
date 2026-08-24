---
page_title: "List Resource: pyvider_directory_entry"
subcategory: "File Operations"
description: |-
  Lists files in a directory.
---

# pyvider_directory_entry (List Resource)

Lists files in a directory.

List resources are queried with `terraform query` from a `.tfquery.hcl` file
rather than planned or applied. The schema below is the `config` block of the
`list` block, not the schema of the managed resource being listed.

## Example Usage

{{ example("example") }}

{{ schema() }}
