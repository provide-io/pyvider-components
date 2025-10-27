---
page_title: "Resource: pyvider_timed_token"
description: |-
  Generate short-lived tokens for tests and demos.
---

# pyvider_timed_token (Resource)

Produce a UUID-backed token that expires automatically. Designed for samples and integration tests that need temporary credentials.

## Example

{{ example("basic") }}

## Schema

{{ schema() }}

## Notes

- `token` and `token_id` are marked sensitive; reference them indirectly when possible.
- `expires_at` reports the ISO timestamp when the token becomes invalid (defaults to one hour after creation).
- Best suited for mock or ephemeral environments rather than production authentication.
