locals {
  add_add_result = provider::pyvider::add(5, 3) # 8
}

output "add_add_result" {
  value = local.add_add_result
}
