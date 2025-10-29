locals {
  divide_result = provider::pyvider::divide(12, 3) # 4
}

output "divide_example" {
  value = local.divide_result
}
