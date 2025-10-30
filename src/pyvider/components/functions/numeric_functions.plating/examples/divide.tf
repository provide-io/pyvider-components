locals {
  divide_divide_result = provider::pyvider::divide(12, 3) # 4
}

output "divide_divide_result" {
  value = local.divide_divide_result
}
