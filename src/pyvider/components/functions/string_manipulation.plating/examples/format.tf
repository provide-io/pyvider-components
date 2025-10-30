locals {
  format_message = provider::pyvider::format("User {} has {} roles.", ["admin", 3])
  # "User admin has 3 roles."
}

output "format_example" {
  value = local.format_message
}
