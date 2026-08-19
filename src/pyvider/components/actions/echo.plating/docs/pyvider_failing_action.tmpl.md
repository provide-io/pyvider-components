---
page_title: "Action: pyvider_failing_action"
subcategory: "Test Mode"
description: |-
  Fails partway through, so the error path is observable from the CLI.
---

# pyvider_failing_action (Action)

Fails partway through, so the error path is observable from the CLI.

Actions run as a side effect of an apply. They are either triggered from a
resource's `lifecycle.action_trigger` block or invoked directly.

## Example Usage

{{ example("example") }}

{{ schema() }}
