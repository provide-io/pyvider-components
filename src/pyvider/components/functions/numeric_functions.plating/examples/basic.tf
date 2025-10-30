# Basic numeric operations
locals {
  basic_numbers = [10, 20, 30]

  total = provider::pyvider::sum(local.basic_numbers)  # 60
  basic_average = provider::pyvider::divide(local.total, 3)  # 20
  rounded = provider::pyvider::round(3.14159, 2)  # 3.14
}

output "basic_numbers" {
  value = {
    total = local.total
    average = local.basic_average
    rounded = local.rounded
  }
}
