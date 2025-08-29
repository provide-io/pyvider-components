---
page_title: "Function: lens_jq"
description: |-
  Applies a jq query and returns a native Python object.
---

# lens_jq (Function)

Applies a jq query and returns a native Python object.

## Example Usage

```terraform
locals {
  example_result = lens_jq(
    # Function arguments here
  )
}

output "function_result" {
  description = "Result of lens_jq function"  
  value       = local.example_result
}

```

## Signature

``

## Arguments



