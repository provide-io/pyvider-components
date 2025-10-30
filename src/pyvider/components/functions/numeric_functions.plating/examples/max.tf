locals {
  max_max_numbers = [10, 5, 8, 2, 15]
  max_max_result = provider::pyvider::max(local.max_max_numbers) # 15
}

output "max_max_result" {
  value = local.max_max_result
}
