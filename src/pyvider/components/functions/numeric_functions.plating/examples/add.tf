locals {
  result = provider::pyvider::add(5, 3) # 8
}

output "add_example" {
  value = local.result
}
