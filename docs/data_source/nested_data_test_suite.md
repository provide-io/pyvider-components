---
page_title: "Data Source: nested_data_test_suite"
description: |-
  Terraform data_source for nested_data_test_suite
---

# nested_data_test_suite (Data Source)

Terraform data_source for nested_data_test_suite

## Example Usage

```terraform
locals {
  example_result = pyvider_nested_data_processor(
    # Function arguments here
  )
}

output "function_result" {
  description = "Result of pyvider_nested_data_processor function"  
  value       = local.example_result
}

```

## Argument Reference

