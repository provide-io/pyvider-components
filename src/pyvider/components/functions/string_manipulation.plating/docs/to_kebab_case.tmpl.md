---
page_title: "Function: to_kebab_case"
description: |-
  Converts text to kebab-case format with lowercase letters and hyphens
---

# to_kebab_case (Function)

> Converts text to kebab-case format by replacing separators with hyphens and using lowercase

The `to_kebab_case` function converts text to kebab-case format, which uses lowercase letters with hyphens separating words. This format is commonly used in URLs, CSS classes, and HTML attributes.

## When to Use This

- **URL slugs**: Create SEO-friendly URLs from page titles
- **CSS class names**: Generate consistent CSS class naming
- **HTML attributes**: Create valid HTML data attributes
- **File names**: Generate web-safe filenames
- **Configuration keys**: Use in systems that prefer kebab-case

**Anti-patterns (when NOT to use):**
- JavaScript variable names (use camelCase instead)
- Database column names (use snake_case instead)
- When preserving original case is important
- For content that needs to remain readable

## Quick Start

```terraform
# Convert page title to URL slug
locals {
  page_title = "User Profile Settings"
  url_slug = provider::pyvider::to_kebab_case(local.page_title)  # Returns: "user-profile-settings"
}

# Convert to CSS class name
variable "component_name" {
  default = "navigationMenu"
}

locals {
  css_class = provider::pyvider::to_kebab_case(var.component_name)  # Returns: "navigation-menu"
}
```

## Examples

### Basic Usage

{{ example("basic") }}

### URL Generation

{{ example("url_generation") }}

### CSS Integration

{{ example("css_integration") }}

## Schema

{{ schema() }}

## Related Functions

- [`to_snake_case`](./to_snake_case.md) - Convert to snake_case format
- [`to_camel_case`](./to_camel_case.md) - Convert to camelCase format
- [`lower`](./lower.md) - Convert to lowercase
- [`replace`](./replace.md) - Replace specific text patterns
- [`split`](./split.md) - Split strings for processing