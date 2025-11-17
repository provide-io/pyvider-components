---
page_title: "Data Source: pyvider_structured_object_test"
description: |-
  Test data source for validating structured object handling with nested attributes
---

# pyvider_structured_object_test (Data Source)

**Note:** This is a test-only data source. Enable with `provider_testmode = true`.

Test data source for validating structured object handling with well-defined nested attributes. Takes a required config name and optional metadata map, returns generated configuration objects and summary information with nested structures.

## Example Usage

{{ example("basic") }}

{{ example("with_metadata") }}

## Argument Reference

{{ schema() }}
