locals {
  subtract_subtract_result = provider::pyvider::subtract(10, 4) # 6
}

output "subtract_subtract_result" {
  value = local.subtract_subtract_result
}
