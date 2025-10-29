locals {
  subtract_result = provider::pyvider::subtract(10, 4) # 6
}

output "subtract_example" {
  value = local.subtract_result
}
