---
page_title: "Function: lens_jq"
description: |-
  Run jq queries against Terraform values.
---

# lens_jq (Function)

Apply jq expressions to maps, lists, or JSON strings when the lens capability is enabled in the provider configuration.

## Example

{{ example("basic") }}

## Signature

`lens_jq(data: any, query: string) -> any`

## Parameters

- `data` (any, required) — Value to inspect. Accepts Terraform collections and primitives.
- `query` (string, required) — jq expression to evaluate. Must be a non-empty string.

## Returns

The jq result converted back to native Terraform types.

## Notes

- The provider must enable the `lens` capability; otherwise a `FunctionError` is raised.
- Unexpected jq errors surface directly from the underlying engine.
