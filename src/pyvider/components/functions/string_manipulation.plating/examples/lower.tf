locals {
  lower_username = provider::pyvider::lower("ADMIN@EXAMPLE.COM") # "admin@example.com"
}

output "lower_example" {
  value = local.lower_username
}
