---
page_title: "Function: pyvider_nested_data_processor"
subcategory: "Test Mode"
description: |-
  Parses a JSON string and returns a summarised JSON string.
---

# pyvider_nested_data_processor (Function)

Parses a JSON string and returns a JSON string carrying the original data
alongside a summary of it. `processing_mode` selects what the summary
contains. Invalid JSON is reported as a function error rather than being
silently treated as empty.

## Example Usage

{{ example("example") }}

## Signature

`{{ signature_markdown }}`

## Arguments

{{ arguments_markdown }}

{% if has_variadic %}
## Variadic Arguments

{{ variadic_argument_markdown }}
{% endif %}
