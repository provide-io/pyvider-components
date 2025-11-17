locals {
  numbers = [10, 5, 8, 2, 15]
  result = provider::pyvider::sum(local.numbers) # 40
}

output "sum_example" {
  value = local.result
}
