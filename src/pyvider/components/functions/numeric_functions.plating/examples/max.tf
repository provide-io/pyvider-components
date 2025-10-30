locals {
  numbers = [10, 5, 8, 2, 15]
  result = provider::pyvider::max(local.numbers) # 15
}

output "max_example" {
  value = local.result
}
