---
page_title: "Function: to_kebab_case"
description: |-
  Convert text to kebab-case.
---

# to_kebab_case (Function)

Transform input text to lowercase words separated by hyphens.

## Example

```terraform
locals {
  slug = provider::pyvider::to_kebab_case("Release Candidate 1") # "release-candidate-1"
}
```

## Signature

`to_kebab_case(text: string) -> string`

## Parameters

- `text` (string, required) — Text to transform. Returns `null` for `null` input.

## Returns

The kebab-case string.
