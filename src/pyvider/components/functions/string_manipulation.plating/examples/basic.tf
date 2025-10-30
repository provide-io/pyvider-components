# Basic string manipulation
locals {
  basic_text = "Hello World"

  uppercase = provider::pyvider::upper(local.basic_text)  # "HELLO WORLD"
  lowercase = provider::pyvider::lower(local.basic_text)  # "hello world"
  formatted = provider::pyvider::format("Name: {}", ["Alice"])  # "Name: Alice"
}

output "basic_text" {
  value = {
    upper = local.uppercase
    lower = local.lowercase
    formatted = local.formatted
  }
}
