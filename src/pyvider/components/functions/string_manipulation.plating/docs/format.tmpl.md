page_title: "Function: format"
description: |-
  Format a template string with positional arguments.
---

# format (Function)

Substitute `{}` placeholders in a template with values. Inputs are coerced with `tostring`, letting you mix strings, numbers, and booleans safely.

## Example

{{ example("basic") }}

## Signature

`format(template: string, values: list[any]) -> string`

## Parameters

- `template` (string, required) — String containing `{}` placeholders. Returns `null` when the template is `null`.
- `values` (list[any], required) — Positional values inserted into the template. A `null` list is treated as empty.

## Returns

A formatted string or `null` when the template is `null`.

## Notes

- Values are converted with `tostring` before substitution.
- Not enough values for the template raises a `FunctionError`.
  clear_template = "User {} logged in from {} at {}"
  message = provider::pyvider::format(local.clear_template, [var.user, var.ip, var.timestamp])
}

# ❌ Avoid - unclear placeholder order
locals {
  unclear_template = "Event: {} {} {} {}"
  # Hard to know which value goes where
}
```

### 3. Handle Different Data Types
```terraform
locals {
  mixed_values = [
    var.string_value,
    var.number_value,
    var.boolean_value
  ]

  formatted = provider::pyvider::format(
    "Config: {}, Count: {}, Enabled: {}",
    local.mixed_values
  )
}
```

## Related Functions

- [`replace`](./replace.md) - Replace specific patterns in strings
- [`join`](./join.md) - Join list elements with delimiters
- [`upper`](./upper.md) - Convert formatted strings to uppercase
- [`lower`](./lower.md) - Convert formatted strings to lowercase
