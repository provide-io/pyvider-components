locals {
  multiply_multiply_result = provider::pyvider::multiply(4, 3) # 12
}

output "multiply_multiply_result" {
  value = local.multiply_multiply_result
}
