locals {
  numbers = [10, 5, 8, 2, 15]
  result = provider::pyvider::min(local.numbers) # 2
}

output "min_example" {
  value = local.result
}
