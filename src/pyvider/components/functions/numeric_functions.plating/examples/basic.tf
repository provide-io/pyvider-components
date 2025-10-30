# Basic numeric operations
locals {
  numbers = [10, 20, 30]

  total = provider::pyvider::sum(local.numbers)  # 60
  average = provider::pyvider::divide(local.total, 3)  # 20
  rounded = provider::pyvider::round(3.14159, 2)  # 3.14
}

output "basic_math" {
  value = {
    total = local.total
    average = local.average
    rounded = local.rounded
  }
}
