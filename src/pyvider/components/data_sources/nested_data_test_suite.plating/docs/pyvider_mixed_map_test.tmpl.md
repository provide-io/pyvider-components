---
page_title: "Data Source: pyvider_mixed_map_test"
description: |-
  Test data source for validating mixed-type map handling with dynamic values
---

# pyvider_mixed_map_test (Data Source)

**Note:** This is a test-only data source. Enable with `provider_testmode = true`.

Test data source for validating mixed-type map handling with dynamic values. Takes an optional map with mixed types (strings, numbers, etc.) as input, processes each value according to its type (strings to uppercase, numbers +1), and returns the processed map with a hash.

## Example Usage

{{ example("mixed") }}

## Argument Reference

{{ schema() }}
