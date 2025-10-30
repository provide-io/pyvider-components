locals {
  length_length_numbers = [1, 2, 3, 4, 5]
  length_length_result = provider::pyvider::length(local.length_length_numbers) # 5
}

output "length_length_result" {
  value = local.length_length_result
}
