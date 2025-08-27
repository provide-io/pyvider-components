---
page_title: "Resource: pyvider_nested_resource_test"
description: |-
  A diagnostic resource for testing nested block and dynamic attribute handling.
---

# pyvider_nested_resource_test (Resource)

This is a diagnostic resource used to test and validate the framework's ability to correctly handle complex, nested data structures within a resource's state.

It accepts a dynamic `configuration` map and a list of `nested_configs` blocks. The resource's primary function is to process this nested data and reflect it in its computed attributes, confirming that the framework's data marshalling and state management are working correctly for complex schemas.

## Example Usage

{{ example("example") }}

## Argument Reference

{{ schema() }}
