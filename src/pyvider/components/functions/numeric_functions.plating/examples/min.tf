locals {
  min_min_numbers = [10, 5, 8, 2, 15]
  min_min_result = provider::pyvider::min(local.min_min_numbers) # 2
}

output "min_min_result" {
  value = local.min_min_result
}
