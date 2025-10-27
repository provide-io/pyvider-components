---
page_title: "Resource: pyvider_private_state_verifier"
description: |-
  Demonstrate private state encryption for provider development.
---

# pyvider_private_state_verifier (Resource)

Utility resource for testing the provider’s private-state handling. It generates a derived token from `input_value` and stores the sensitive version in Terraform’s encrypted private state.

## Example

{{ example("basic") }}

## Schema

{{ schema() }}

## Notes

- Intended for validation and demos; do not use in production plans.
- `decrypted_token` is computed during apply so you can confirm encryption/decryption works end to end.
- Input and outputs are simple strings—pair with test frameworks or CI jobs when exercising the provider.
