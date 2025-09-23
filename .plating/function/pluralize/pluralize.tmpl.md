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

## Common Patterns

### File System Reports
```terraform
variable "directory_stats" {
  type = list(object({
    path = string
    file_count = number
    folder_count = number
    size_bytes = number
  }))
  default = [
    {
      path = "/home/user/documents"
      file_count = 23
      folder_count = 4
      size_bytes = 1073741824
    },
    {
      path = "/var/log"
      file_count = 156
      folder_count = 12
      size_bytes = 536870912
    }
  ]
}

locals {
  directory_reports = [
    for dir in var.directory_stats : {
      path = dir.path
      summary = join(", ", [
        "${dir.file_count} ${provider::pyvider::pluralize("file", dir.file_count)}",
        "${dir.folder_count} ${provider::pyvider::pluralize("folder", dir.folder_count)}",
        provider::pyvider::format_size(dir.size_bytes, 1)
      ])
    }
  ]
}

resource "pyvider_file_content" "directory_report" {
  filename = "/tmp/directory_stats.txt"
  content = join("\n", concat(
    ["=== Directory Statistics ===", ""],
    [
      for report in local.directory_reports :
      "${report.path}: ${report.summary}"
    ]
  ))
}
```

### User Activity Summary
```terraform
variable "user_activities" {
  type = list(object({
    username = string
    login_count = number
    message_count = number
    document_count = number
  }))
  default = [
    {
      username = "alice"
      login_count = 1
      message_count = 0
      document_count = 15
    },
    {
      username = "bob"
      login_count = 23
      message_count = 7
      document_count = 3
    }
  ]
}

locals {
  activity_summaries = [
    for activity in var.user_activities : {
      username = activity.username
      login_summary = "${activity.login_count} ${provider::pyvider::pluralize("login", activity.login_count)}"
      message_summary = "${activity.message_count} ${provider::pyvider::pluralize("message", activity.message_count)}"
      document_summary = "${activity.document_count} ${provider::pyvider::pluralize("document", activity.document_count)}"
    }
  ]
}
```

### Error Message Generation
```terraform
variable "validation_results" {
  type = list(object({
    field = string
    error_count = number
    warning_count = number
  }))
  default = [
    { field = "email", error_count = 1, warning_count = 0 },
    { field = "password", error_count = 3, warning_count = 1 },
    { field = "username", error_count = 0, warning_count = 2 }
  ]
}

locals {
  validation_messages = [
    for result in var.validation_results : {
      field = result.field
      has_errors = result.error_count > 0
      has_warnings = result.warning_count > 0
      error_text = result.error_count > 0 ?
        "${result.error_count} ${provider::pyvider::pluralize("error", result.error_count)}" :
        ""
      warning_text = result.warning_count > 0 ?
        "${result.warning_count} ${provider::pyvider::pluralize("warning", result.warning_count)}" :
        ""
      summary = join(" and ", compact([local.error_text, local.warning_text]))
    }
  ]
}
```

### Notification System
```terraform
variable "notification_counts" {
  type = object({
    unread_email = number
    pending_task = number
    new_comment = number
    system_alert = number
  })
  default = {
    unread_email = 5
    pending_task = 1
    new_comment = 0
    system_alert = 2
  }
}

locals {
  notifications = [
    {
      type = "email"
      count = var.notification_counts.unread_email
      message = var.notification_counts.unread_email > 0 ?
        "You have ${var.notification_counts.unread_email} unread ${provider::pyvider::pluralize("email", var.notification_counts.unread_email)}" :
        "No unread emails"
    },
    {
      type = "task"
      count = var.notification_counts.pending_task
      message = var.notification_counts.pending_task > 0 ?
        "${var.notification_counts.pending_task} ${provider::pyvider::pluralize("task", var.notification_counts.pending_task)} pending" :
        "No pending tasks"
    },
    {
      type = "comment"
      count = var.notification_counts.new_comment
      message = var.notification_counts.new_comment > 0 ?
        "${var.notification_counts.new_comment} new ${provider::pyvider::pluralize("comment", var.notification_counts.new_comment)}" :
        "No new comments"
    }
  ]

  active_notifications = [for n in local.notifications : n if n.count > 0]
}
```

## Pluralization Rules

### Standard Rules
The function follows English pluralization patterns:

| Singular | Count | Result |
|----------|-------|--------|
| "file" | 1 | "file" |
| "file" | 0, 2+ | "files" |
| "box" | 1 | "box" |
| "box" | 0, 2+ | "boxes" |
| "city" | 1 | "city" |
| "city" | 0, 2+ | "cities" |

### Custom Plural Forms
For irregular plurals, provide the custom form:

| Singular | Count | Custom Plural | Result |
|----------|-------|---------------|--------|
| "child" | 1 | "children" | "child" |
| "child" | 0, 2+ | "children" | "children" |
| "person" | 1 | "people" | "person" |
| "person" | 0, 2+ | "people" | "people" |
| "mouse" | 1 | "mice" | "mouse" |
| "mouse" | 0, 2+ | "mice" | "mice" |

## Count Handling

### Special Cases
```terraform
locals {
  # Zero count uses plural
  zero_files = provider::pyvider::pluralize("file", 0)  # Returns: "files"

  # One uses singular
  one_file = provider::pyvider::pluralize("file", 1)    # Returns: "file"

  # Negative counts use plural
  negative = provider::pyvider::pluralize("item", -5)   # Returns: "items"

  # Decimal counts use plural
  decimal = provider::pyvider::pluralize("hour", 1.5)   # Returns: "hours"
}
```

## Error Handling

### Null Input
```terraform
locals {
  # Returns null for null word
  null_word = provider::pyvider::pluralize(null, 5)     # Returns: null

  # Handles null count as 0 (plural)
  null_count = provider::pyvider::pluralize("item", null)  # Returns: "items"
}
```

### Empty String
```terraform
locals {
  # Returns empty string for empty word
  empty_word = provider::pyvider::pluralize("", 5)      # Returns: ""
}
```

### Invalid Custom Plural
```terraform
locals {
  # Empty custom plural falls back to standard rules
  empty_custom = provider::pyvider::pluralize("box", 5, "")  # Returns: "boxes"

  # Null custom plural falls back to standard rules
  null_custom = provider::pyvider::pluralize("box", 5, null)  # Returns: "boxes"
}
```

## Best Practices

### 1. Use with Conditional Logic
```terraform
variable "item_count" {
  type = number
  validation {
    condition     = var.item_count >= 0
    error_message = "Count cannot be negative."
  }
}

locals {
  status_message = var.item_count == 0 ?
    "No items found" :
    "Found ${var.item_count} ${provider::pyvider::pluralize("item", var.item_count)}"
}
```

### 2. Handle Irregular Plurals
```terraform
# Keep a mapping of irregular plurals
locals {
  irregular_plurals = {
    "child" = "children"
    "person" = "people"
    "mouse" = "mice"
    "foot" = "feet"
    "tooth" = "teeth"
    "goose" = "geese"
  }
}

# Use in pluralization
locals {
  word = "child"
  count = 3
  pluralized = provider::pyvider::pluralize(
    word,
    count,
    lookup(local.irregular_plurals, word, null)
  )
}
```

### 3. Combine with Formatting
```terraform
variable "statistics" {
  type = map(number)
  default = {
    users = 1234
    posts = 5678
    comments = 12345
  }
}

locals {
  formatted_stats = [
    for key, value in var.statistics :
    "${value} ${provider::pyvider::pluralize(key, value)}"
  ]

  stats_summary = "Database contains ${join(", ", local.formatted_stats)}"
}
```

## Language Considerations

### English Rules Only
This function implements English pluralization rules. For other languages:

```terraform
# For non-English, you might need conditional logic
variable "language" {
  type = string
  default = "en"
}

locals {
  # Only use pluralize for English
  message = var.language == "en" ?
    "${var.count} ${provider::pyvider::pluralize("item", var.count)}" :
    "${var.count} items"  # Fallback for other languages
}
```

## Performance Considerations

- **Rule-based processing**: Efficient pattern matching for pluralization
- **Memory efficient**: Minimal memory allocation
- **Fast execution**: Quick string operations
- **Caching friendly**: Deterministic results suitable for caching

## Related Functions

- [`tostring`](./tostring.md) - Convert numbers to strings for messages
- [`format`](./format.md) - Format strings with placeholders
- [`join`](./join.md) - Join multiple message parts
- [`contains`](./contains.md) - Check for specific words or patterns
- [`replace`](./replace.md) - Replace text in generated messages