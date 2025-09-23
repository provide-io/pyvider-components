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

## Common Patterns

### Article Preview Generation
```terraform
variable "blog_posts" {
  type = list(object({
    title = string
    content = string
    author = string
  }))
  default = [
    {
      title = "Getting Started with Infrastructure as Code"
      content = "Infrastructure as Code (IaC) is a method of managing and provisioning computing infrastructure through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools. This approach brings many benefits including version control, reproducibility, and automation capabilities that traditional infrastructure management lacks."
      author = "Jane Smith"
    },
    {
      title = "Advanced Terraform Techniques for Large Scale Deployments"
      content = "When working with Terraform at scale, several patterns and techniques become essential for maintaining clean, efficient, and manageable code. This article explores advanced concepts including module composition, state management strategies, and automation patterns that help teams successfully deploy infrastructure across multiple environments."
      author = "John Doe"
    }
  ]
}

locals {
  # Create article previews
  article_previews = [
    for post in var.blog_posts : {
      title = provider::pyvider::truncate(post.title, 40, "...")
      preview = provider::pyvider::truncate(post.content, 150, "... [Read more]")
      author = post.author
    }
  ]
}

resource "pyvider_file_content" "blog_preview" {
  filename = "/tmp/blog_previews.html"
  content = join("\n", [
    for preview in local.article_previews :
    "<article>\n  <h3>${preview.title}</h3>\n  <p>${preview.preview}</p>\n  <small>By ${preview.author}</small>\n</article>"
  ])
}
```

### Log Message Formatting
```terraform
variable "log_entries" {
  type = list(object({
    timestamp = string
    level = string
    message = string
    source = string
  }))
  default = [
    {
      timestamp = "2024-01-15T10:30:15Z"
      level = "ERROR"
      message = "Database connection failed after 3 retry attempts. Connection timeout exceeded while trying to establish connection to primary database server at db1.example.com:5432. This error may indicate network connectivity issues or database server unavailability."
      source = "DatabaseService"
    },
    {
      timestamp = "2024-01-15T10:30:16Z"
      level = "INFO"
      message = "Successfully established connection to replica database server after fallback from primary server failure."
      source = "DatabaseService"
    }
  ]
}

locals {
  # Format log entries for console display
  formatted_logs = [
    for entry in var.log_entries : {
      timestamp = entry.timestamp
      level = entry.level
      source = provider::pyvider::truncate(entry.source, 15, "")
      message = provider::pyvider::truncate(entry.message, 80, "...")
    }
  ]
}

resource "pyvider_file_content" "log_summary" {
  filename = "/tmp/log_summary.txt"
  content = join("\n", concat(
    ["=== Log Summary ===", ""],
    [
      for entry in local.formatted_logs :
      "[${entry.timestamp}] ${entry.level} ${entry.source}: ${entry.message}"
    ]
  ))
}
```

### File Name Shortening
```terraform
variable "file_paths" {
  type = list(string)
  default = [
    "/very/long/path/to/some/important/configuration/file.yaml",
    "/another/extremely/long/path/to/application/settings/database.json",
    "/short/path/config.xml"
  ]
}

locals {
  # Create shortened file displays
  file_displays = [
    for path in var.file_paths : {
      full_path = path
      display_name = provider::pyvider::truncate(path, 30, "...")
      # Extract just filename for very short display
      filename = basename(path)
    }
  ]
}
```

### Table Cell Formatting
```terraform
variable "user_data" {
  type = list(object({
    id = number
    username = string
    email = string
    bio = string
  }))
  default = [
    {
      id = 1
      username = "alice_johnson_developer"
      email = "alice.johnson.developer@company.example.com"
      bio = "Senior software engineer with expertise in distributed systems, cloud architecture, and DevOps practices. Passionate about building scalable solutions and mentoring junior developers."
    },
    {
      id = 2
      username = "bob_smith_admin"
      email = "bob.smith.admin@company.example.com"
      bio = "System administrator with 10+ years of experience managing enterprise infrastructure and ensuring high availability of critical systems."
    }
  ]
}

resource "pyvider_file_content" "user_table" {
  filename = "/tmp/user_table.csv"
  content = join("\n", concat(
    ["ID,Username,Email,Bio"],
    [
      for user in var.user_data :
      "${user.id},${provider::pyvider::truncate(user.username, 15, "")},${provider::pyvider::truncate(user.email, 25, "...")},${provider::pyvider::truncate(user.bio, 50, "...")}"
    ]
  ))
}
```

## Truncation Strategies

### Word Boundary Truncation
```terraform
# Note: This function truncates at character boundaries
# For word boundary truncation, combine with other functions
locals {
  text = "The quick brown fox jumps over the lazy dog"
  char_truncated = provider::pyvider::truncate(text, 20, "...")  # "The quick brown fo..."

  # For word boundary truncation, you'd need additional logic
  words = provider::pyvider::split(text, " ")
  # Custom logic would be needed to truncate at word boundaries
}
```

### Progressive Truncation
```terraform
variable "content_priorities" {
  type = list(object({
    text = string
    priority = number
  }))
  default = [
    { text = "Critical system alert message", priority = 1 },
    { text = "Important but not urgent notification", priority = 2 },
    { text = "General information message for user awareness", priority = 3 }
  ]
}

locals {
  # Apply different truncation lengths based on priority
  prioritized_content = [
    for item in var.content_priorities :
    provider::pyvider::truncate(
      item.text,
      item.priority == 1 ? 50 : item.priority == 2 ? 30 : 20,
      "..."
    )
  ]
}
```

## Parameters

### Length Parameter
The maximum length includes the suffix:

| Input | Max Length | Suffix | Output |
|-------|------------|--------|--------|
| "Hello World" | 10 | "..." | "Hello W..." |
| "Hello World" | 15 | "..." | "Hello World" |
| "Hello World" | 8 | " more" | "Hel more" |

### Suffix Parameter
```terraform
locals {
  text = "Long text that needs truncation"

  # Different suffix examples
  default_suffix = provider::pyvider::truncate(text, 15)          # "Long text th..."
  custom_suffix = provider::pyvider::truncate(text, 15, " [+]")   # "Long text  [+]"
  no_suffix = provider::pyvider::truncate(text, 15, "")          # "Long text that"
  long_suffix = provider::pyvider::truncate(text, 15, " [more]") # "Long te [more]"
}
```

## Error Handling

### Null Input
```terraform
locals {
  # Returns null for null input
  null_result = provider::pyvider::truncate(null, 10)  # Returns: null
}
```

### Empty String
```terraform
locals {
  # Returns empty string for empty input
  empty_result = provider::pyvider::truncate("", 10)  # Returns: ""
}
```

### Short Text
```terraform
locals {
  # Returns original text if shorter than max length
  short_text = provider::pyvider::truncate("Hello", 10)  # Returns: "Hello"
}
```

### Edge Cases
```terraform
locals {
  # When suffix is longer than max length
  edge_case = provider::pyvider::truncate("Hello", 3, "...")  # Returns: "..."

  # Zero or negative length
  zero_length = provider::pyvider::truncate("Hello", 0, "...")  # Returns: ""
}
```

## Best Practices

### 1. Consider Content Type
```terraform
locals {
  # For titles: shorter truncation
  title = provider::pyvider::truncate(var.page_title, 30, "...")

  # For descriptions: longer truncation
  description = provider::pyvider::truncate(var.page_description, 150, "... [Read more]")

  # For technical content: preserve more context
  code_snippet = provider::pyvider::truncate(var.code_example, 200, "\n... [Continued]")
}
```

### 2. Responsive Truncation
```terraform
variable "display_mode" {
  type = string
  default = "desktop"
  validation {
    condition     = contains(["mobile", "tablet", "desktop"], var.display_mode)
    error_message = "Display mode must be mobile, tablet, or desktop."
  }
}

locals {
  max_length = var.display_mode == "mobile" ? 20 : var.display_mode == "tablet" ? 40 : 60
  truncated_content = provider::pyvider::truncate(var.content, local.max_length, "...")
}
```

### 3. Preserve Important Information
```terraform
locals {
  # For error messages, preserve the beginning
  error_message = "DatabaseConnectionError: Failed to connect to database server at db1.example.com:5432 after 3 retry attempts"
  truncated_error = provider::pyvider::truncate(error_message, 50, "... [See logs]")

  # For file paths, consider showing the end
  long_path = "/very/long/path/to/important/config/file.yaml"
  # This would show beginning; you might want to show the filename instead
  path_display = provider::pyvider::truncate(long_path, 25, "...")
}
```

## Performance Considerations

- **Efficient processing**: Fast string operations with minimal overhead
- **Memory conscious**: No significant memory allocation
- **Length calculation**: Efficient character counting
- **Suffix handling**: Optimized suffix addition logic

## Related Functions

- [`length`](./length.md) - Get string length for truncation decisions
- [`split`](./split.md) - Split text for word-boundary truncation
- [`join`](./join.md) - Rejoin truncated word arrays
- [`replace`](./replace.md) - Replace text patterns
- [`upper`](./upper.md) - Convert case of truncated text