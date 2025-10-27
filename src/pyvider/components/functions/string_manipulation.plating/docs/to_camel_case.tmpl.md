---
page_title: "Function: to_camel_case"
description: |-
  Convert text to camelCase or PascalCase.
---

# to_camel_case (Function)

Normalize identifiers using camelCase by default. Pass a truthy second argument to produce PascalCase instead.

## Example

```terraform
locals {
  variable_name = provider::pyvider::to_camel_case("user_profile")      # "userProfile"
  class_name    = provider::pyvider::to_camel_case("user_profile", true) # "UserProfile"
}
```

## Signature

`to_camel_case(text: string, options: variadic) -> string`

## Parameters

- `text` (string, required) — Text to transform. Returns `null` when this is `null`.
- `options` (variadic, optional) — When present, the first value controls `upper_first`; truthy values request PascalCase.

## Returns

The converted string, or `null` when `text` is `null`.
