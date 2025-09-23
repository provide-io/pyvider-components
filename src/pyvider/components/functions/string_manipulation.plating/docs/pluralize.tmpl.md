---
page_title: "Function: pluralize"
description: |-
  Pluralizes words based on count with support for custom plural forms
---

# pluralize (Function)

> Converts words to plural form based on count with intelligent English pluralization rules

The `pluralize` function converts words to their plural form based on a count value. It automatically applies English pluralization rules and allows custom plural forms for irregular words. Returns singular form for count of 1, plural form otherwise.

## When to Use This

- **User interface messages**: Display grammatically correct messages
- **Report generation**: Create proper text in dynamic reports
- **Notification systems**: Generate contextual notifications
- **Data summaries**: Create readable count descriptions
- **Form validation**: Display appropriate error messages

**Anti-patterns (when NOT to use):**
- For non-English text (function uses English rules)
- When count is always singular or plural
- For technical terms that don't follow standard rules
- When grammar requirements are complex

## Quick Start

```terraform
# Basic pluralization
locals {
  item_count = 5
  message = "${local.item_count} ${provider::pyvider::pluralize("file", local.item_count)}"  # Returns: "5 files"
}

# Custom plural form
locals {
  child_count = 3
  description = "${local.child_count} ${provider::pyvider::pluralize("child", local.child_count, "children")}"  # Returns: "3 children"
}
```

## Examples

### Basic Usage

{{ example("basic") }}

### Report Generation

{{ example("report_generation") }}

### User Interface

{{ example("user_interface") }}

## Schema

{{ schema() }}

## Related Functions

- [`tostring`](./tostring.md) - Convert numbers to strings for messages
- [`format`](./format.md) - Format strings with placeholders
- [`join`](./join.md) - Join multiple message parts
- [`contains`](./contains.md) - Check for specific words or patterns
- [`replace`](./replace.md) - Replace text in generated messages