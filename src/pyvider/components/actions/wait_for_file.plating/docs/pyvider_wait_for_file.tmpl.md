---
page_title: "Action: pyvider_wait_for_file"
subcategory: "File Operations"
description: |-
  Blocks until a path exists, reporting progress while it waits.
---

# pyvider_wait_for_file (Action)

Blocks until a path exists, reporting progress while it waits.

Actions run as a side effect of an apply. They are either triggered from a
resource's `lifecycle.action_trigger` block or invoked directly.

## Example Usage

{{ example("example") }}

{{ schema() }}
