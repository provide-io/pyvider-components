---
page_title: "Function: format_size"
description: |-
  Formats byte values as human-readable file sizes with customizable precision
---

# format_size (Function)

> Converts byte values to human-readable file size strings with automatic unit selection

The `format_size` function formats byte values into human-readable strings using appropriate units (B, KB, MB, GB, TB, PB). It automatically selects the most appropriate unit and allows customizable decimal precision.

## When to Use This

- **File size display**: Show file sizes in user-friendly format
- **Storage reports**: Display storage usage and capacity
- **Bandwidth monitoring**: Format network transfer amounts
- **Memory usage**: Display RAM or cache sizes
- **Progress indicators**: Show download/upload progress

**Anti-patterns (when NOT to use):**
- When exact byte values are needed for calculations
- For non-size numeric values (use appropriate number formatting)
- When binary units (1024-based) are specifically required
- In APIs where raw byte values are expected

## Quick Start

```terraform
# Format file sizes
locals {
  file_sizes = [1024, 1048576, 1073741824]
  formatted_sizes = [
    for size in local.file_sizes :
    provider::pyvider::format_size(size)
  ]
  # Returns: ["1.0 KB", "1.0 MB", "1.0 GB"]
}

# Custom precision
locals {
  large_file = 1234567890
  precise_size = provider::pyvider::format_size(local.large_file, 2)  # Returns: "1.15 GB"
  rounded_size = provider::pyvider::format_size(local.large_file, 0)  # Returns: "1 GB"
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

### Storage Analysis



### File Management



## Schema



## Related Functions

- [`tostring`](./tostring.md) - Convert values to string format
- [`round`](./round.md) - Round numeric values
- [`add`](./add.md) - Add numeric values for totals
- [`multiply`](./multiply.md) - Calculate size multiplications
- [`divide`](./divide.md) - Calculate size divisions