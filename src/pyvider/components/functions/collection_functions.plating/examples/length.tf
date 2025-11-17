locals {
  numbers = [1, 2, 3, 4, 5]
  length_result = provider::pyvider::length(local.numbers) # 5
}

output "length_example" {
  value = local.length_result
}
