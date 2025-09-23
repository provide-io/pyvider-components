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

```terraform
# Basic string manipulation function examples

# Case conversion examples
locals {
  original_text = "Hello World"

  uppercase_text = provider::pyvider::upper(local.original_text)    # Returns: "HELLO WORLD"
  lowercase_text = provider::pyvider::lower(local.original_text)    # Returns: "hello world"
}

# String formatting examples
locals {
  template_string = "Hello, {name}! You have {count} messages."

  formatted_message = provider::pyvider::format(local.template_string, {
    name = "Alice"
    count = 5
  })  # Returns: "Hello, Alice! You have 5 messages."

  # Simple template
  simple_format = provider::pyvider::format("User: {user}", {
    user = "admin"
  })  # Returns: "User: admin"
}

# String joining examples
locals {
  word_list = ["apple", "banana", "cherry"]

  comma_separated = provider::pyvider::join(local.word_list, ", ")     # Returns: "apple, banana, cherry"
  pipe_separated = provider::pyvider::join(local.word_list, " | ")     # Returns: "apple | banana | cherry"
  no_separator = provider::pyvider::join(local.word_list, "")          # Returns: "applebananacherry"
}

# String splitting examples
locals {
  csv_data = "apple,banana,cherry,date"

  split_by_comma = provider::pyvider::split(local.csv_data, ",")       # Returns: ["apple", "banana", "cherry", "date"]

  # Split with limit
  path_string = "/home/user/documents/file.txt"
  split_path = provider::pyvider::split(local.path_string, "/")        # Returns: ["", "home", "user", "documents", "file.txt"]
}

# String replacement examples
locals {
  original_text = "The quick brown fox jumps over the lazy dog"

  replace_fox = provider::pyvider::replace(local.original_text, "fox", "cat")    # Returns: "The quick brown cat jumps over the lazy dog"
  replace_spaces = provider::pyvider::replace(local.original_text, " ", "_")     # Returns: "The_quick_brown_fox_jumps_over_the_lazy_dog"
}

# Combined string operations
locals {
  user_input = "  MiXeD cAsE tExT  "

  # Clean and normalize user input
  cleaned_input = provider::pyvider::lower(
    provider::pyvider::replace(
      provider::pyvider::replace(user_input, "  ", " "),  # Remove extra spaces
      " ", "_"                                            # Replace remaining spaces with underscores
    )
  )  # Returns: "mixed_case_text"

  # Create a filename from user input
  filename = provider::pyvider::format("{base}.{ext}", {
    base = local.cleaned_input
    ext = "txt"
  })  # Returns: "mixed_case_text.txt"
}

# Output results for verification
output "string_manipulation_examples" {
  value = {
    case_conversion = {
      original = local.original_text
      uppercase = local.uppercase_text
      lowercase = local.lowercase_text
    }

    formatting = {
      template = local.template_string
      formatted = local.formatted_message
      simple = local.simple_format
    }

    joining = {
      words = local.word_list
      comma_separated = local.comma_separated
      pipe_separated = local.pipe_separated
      no_separator = local.no_separator
    }

    splitting = {
      csv_original = local.csv_data
      csv_split = local.split_by_comma
      path_original = local.path_string
      path_split = local.split_path
    }

    replacement = {
      original = local.original_text
      fox_to_cat = local.replace_fox
      spaces_to_underscores = local.replace_spaces
    }

    combined_operations = {
      user_input = user_input
      cleaned = local.cleaned_input
      filename = local.filename
    }
  }
}
```

### Content Management



### UI Display



## Schema



## Related Functions

- [`length`](./length.md) - Get string length for truncation decisions
- [`split`](./split.md) - Split text for word-boundary truncation
- [`join`](./join.md) - Rejoin truncated word arrays
- [`replace`](./replace.md) - Replace text patterns
- [`upper`](./upper.md) - Convert case of truncated text