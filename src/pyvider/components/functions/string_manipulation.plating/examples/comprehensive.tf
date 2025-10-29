# Basic string manipulation function examples

# Case conversion examples
locals {
  comp_case_original_text = "Hello World"

  comp_uppercase_text = provider::pyvider::upper(local.comp_case_original_text)    # Returns: "HELLO WORLD"
  comp_lowercase_text = provider::pyvider::lower(local.comp_case_original_text)    # Returns: "hello world"
}

# String formatting examples
locals {
  comp_template_string = "Hello, {}! You have {} messages."

  formatted_message = provider::pyvider::format(local.comp_template_string, [
    "Alice",
    5
  ])  # Returns: "Hello, Alice! You have 5 messages."

  # Simple template
  simple_format = provider::pyvider::format("User: {}", [
    "admin"
  ])  # Returns: "User: admin"
}

# String joining examples
locals {
  comp_word_list = ["apple", "banana", "cherry"]

  comp_comma_separated = provider::pyvider::join(local.comp_word_list, ", ")     # Returns: "apple, banana, cherry"
  comp_pipe_separated = provider::pyvider::join(local.comp_word_list, " | ")     # Returns: "apple | banana | cherry"
  comp_no_separator = provider::pyvider::join(local.comp_word_list, "")          # Returns: "applebananacherry"
}

# String splitting examples
locals {
  comp_csv_data = "apple,banana,cherry,date"

  comp_split_by_comma = provider::pyvider::split(local.comp_csv_data, ",")       # Returns: ["apple", "banana", "cherry", "date"]

  # Split with limit
  comp_path_string = "/REDACTED_ABS_PATH"
  comp_split_path = provider::pyvider::split(local.comp_path_string, "/")        # Returns: ["", "home", "user", "documents", "file.txt"]
}

# String replacement examples
locals {
  comp_replacement_original_text = "The quick brown fox jumps over the lazy dog"

  comp_replace_fox = provider::pyvider::replace(local.comp_replacement_original_text, "fox", "cat")    # Returns: "The quick brown cat jumps over the lazy dog"
  comp_replace_spaces = provider::pyvider::replace(local.comp_replacement_original_text, " ", "_")     # Returns: "The_quick_brown_fox_jumps_over_the_lazy_dog"
}

# Combined string operations
locals {
  comp_user_input = "  MiXeD cAsE tExT  "

  # Clean and normalize user input
  comp_cleaned_input = provider::pyvider::lower(
    provider::pyvider::replace(
      provider::pyvider::replace(local.comp_user_input, "  ", " "),  # Remove extra spaces
      " ", "_"                                                   # Replace remaining spaces with underscores
    )
  )  # Returns: "mixed_case_text"

  # Create a filename from user input
  comp_filename = provider::pyvider::format("{}.{}", [
    local.comp_cleaned_input,
    "txt"
  ])  # Returns: "mixed_case_text.txt"
}

# Output results for verification
output "string_manipulation_examples" {
  value = {
    case_conversion = {
      original = local.comp_case_original_text
      uppercase = local.comp_uppercase_text
      lowercase = local.comp_lowercase_text
    }

    formatting = {
      template = local.comp_template_string
      formatted = local.formatted_message
      simple = local.simple_format
    }

    joining = {
      words = local.comp_word_list
      comma_separated = local.comp_comma_separated
      pipe_separated = local.comp_pipe_separated
      no_separator = local.comp_no_separator
    }

    splitting = {
      csv_original = local.comp_csv_data
      csv_split = local.comp_split_by_comma
      path_original = local.comp_path_string
      path_split = local.comp_split_path
    }

    replacement = {
      original = local.comp_replacement_original_text
      fox_to_cat = local.comp_replace_fox
      spaces_to_underscores = local.comp_replace_spaces
    }

    combined_operations = {
      user_input = local.comp_user_input
      cleaned = local.comp_cleaned_input
      filename = local.comp_filename
    }
  }
}