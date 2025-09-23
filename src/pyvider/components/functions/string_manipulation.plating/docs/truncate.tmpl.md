---
page_title: "Function: truncate"
description: |-
  Truncates text to a specified length with customizable suffix
---

# truncate (Function)

> Shortens text to a specified maximum length while preserving readability with optional suffix

The `truncate` function shortens text to a specified maximum length, adding a suffix (like "...") to indicate truncation. It's useful for creating previews, fitting text into limited display space, and maintaining consistent text lengths.

## When to Use This

- **Text previews**: Create excerpt previews for articles or descriptions
- **UI constraints**: Fit text into limited display areas
- **List formatting**: Maintain consistent text lengths in lists
- **Table displays**: Prevent text overflow in table cells
- **Log summaries**: Create shortened log entries for overviews

**Anti-patterns (when NOT to use):**
- When full text must always be preserved
- For text that's already within the desired length
- When truncation would remove critical information
- For structured data that requires complete content

## Quick Start

```terraform
# Basic text truncation
locals {
  long_description = "This is a very long description that needs to be shortened for display purposes"
  short_preview = provider::pyvider::truncate(local.long_description, 30)  # Returns: "This is a very long descrip..."
}

# Custom suffix
locals {
  article_title = "Advanced Terraform Provider Development Best Practices"
  truncated_title = provider::pyvider::truncate(local.article_title, 25, " [more]")  # Returns: "Advanced Terraform Pro [more]"
}
```

## Examples

### Basic Usage

{{ example("basic") }}

### Content Management

{{ example("content_management") }}

### UI Display

{{ example("ui_display") }}

## Schema

{{ schema() }}

## Related Functions

- [`length`](./length.md) - Get string length for truncation decisions
- [`split`](./split.md) - Split text for word-boundary truncation
- [`join`](./join.md) - Rejoin truncated word arrays
- [`replace`](./replace.md) - Replace text patterns
- [`upper`](./upper.md) - Convert case of truncated text