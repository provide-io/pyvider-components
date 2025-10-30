---
page_title: "Data Source: pyvider_simple_map_test"
description: |-
  Test data source for validating simple string map handling
---

# pyvider_simple_map_test (Data Source)

**Note:** This is a test-only data source. Enable with `provider_testmode = true`.

Test data source for validating simple string map handling in the CTY type system. Takes an optional map of strings as input, converts all values to uppercase, and returns the processed map along with a SHA256 hash.

## Example Usage

{{ example("simple") }}

{{ example("empty") }}

## Argument Reference

{{ schema() }}
