locals {
  result = provider::pyvider::multiply(4, 3) # 12
}

output "multiply_example" {
  value = local.result
}
