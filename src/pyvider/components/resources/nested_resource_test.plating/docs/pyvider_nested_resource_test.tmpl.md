---
page_title: "Resource: pyvider_nested_resource_test"
subcategory: "Test Mode"
description: |-
  Exercises dynamic attributes and nested block lists end to end.
---

# pyvider_nested_resource_test (Resource)

Exercises dynamic attributes and nested block lists end to end: a `dynamic`
configuration map that Terraform cannot type ahead of apply, and a repeated
`nested_configs` block whose contents are echoed back through a computed
attribute. It exists so the framework's handling of both has something to
prove itself against.

## Example Usage

{{ example("example") }}

{{ schema() }}

## Import

```bash
terraform import pyvider_nested_resource_test.example <id>
```
