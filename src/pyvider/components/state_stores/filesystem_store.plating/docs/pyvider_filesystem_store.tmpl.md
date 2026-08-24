---
page_title: "State Store: pyvider_filesystem_store"
subcategory: "State Storage"
description: |-
  ``FileSystemStateStore`` with a Terraform configuration schema.
---

# pyvider_filesystem_store (State Store)

``FileSystemStateStore`` with a Terraform configuration schema.

State stores are configured inside the `terraform` block and hold Terraform
state on the provider's behalf. Because the store is loaded before the provider
is configured, its own `provider` block is declared inline.

## Example Usage

{{ example("example") }}

{{ schema() }}
