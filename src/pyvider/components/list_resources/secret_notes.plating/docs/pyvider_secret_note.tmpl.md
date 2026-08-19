---
page_title: "List Resource: pyvider_secret_note"
subcategory: "Test Mode"
description: |-
  Lists the secret notes created in this provider process.
---

# pyvider_secret_note (List Resource)

Lists the secret notes created in this provider process.

List resources are queried with `terraform query` from a `.tfquery.hcl` file
rather than planned or applied. The schema below is the `config` block of the
`list` block, not the schema of the managed resource being listed.

## Example Usage

{{ example("example") }}

{{ schema() }}
