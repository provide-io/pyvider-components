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

### Report Generation



### User Interface



## Schema



## Related Functions

- [`tostring`](./tostring.md) - Convert numbers to strings for messages
- [`format`](./format.md) - Format strings with placeholders
- [`join`](./join.md) - Join multiple message parts
- [`contains`](./contains.md) - Check for specific words or patterns
- [`replace`](./replace.md) - Replace text in generated messages