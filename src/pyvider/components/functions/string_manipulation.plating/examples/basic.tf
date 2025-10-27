# Basic string manipulation
locals {
  text = "Hello World"

  uppercase = provider::pyvider::upper(local.text)  # "HELLO WORLD"
  lowercase = provider::pyvider::lower(local.text)  # "hello world"
  formatted = provider::pyvider::format("Name: {}", ["Alice"])  # "Name: Alice"
}

output "basic_strings" {
  value = {
    upper = local.uppercase
    lower = local.lowercase
    formatted = local.formatted
  }
}
