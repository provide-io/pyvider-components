---
page_title: "Data Source: pyvider_provider_config_reader"
description: |-
  Inspect the current pyvider provider configuration.
---

# pyvider_provider_config_reader (Data Source)

Expose values from the active `provider "pyvider"` block so you can branch on endpoints, timeouts, retries, and other settings inside Terraform.

## Example

{{ example("basic") }}

## Schema

{{ schema() }}

## Notes

- Useful for surfacing items such as `api_endpoint`, `api_timeout`, and capability flags.
- Sensitive fields like `api_token` remain marked sensitive in outputs.
- Combine with local logic to adapt behavior per environment without duplicating configuration.
