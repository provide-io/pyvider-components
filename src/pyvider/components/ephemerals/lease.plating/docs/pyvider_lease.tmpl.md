---
page_title: "Ephemeral Resource: pyvider_lease"
subcategory: "Coordination"
description: |-
  Holds a lease on a file for as long as Terraform needs it.
---

# pyvider_lease (Ephemeral Resource)

Holds a lease on a file for as long as Terraform needs it.

Ephemeral resources are opened during an operation and closed when it ends.
Their values are never written to state, so they can only be consumed by
write-only attributes, provider configuration, or other ephemeral values.

## Example Usage

{{ example("example") }}

{{ schema() }}
