# Basic type conversion
locals {
  number = 42
  basic_boolean = true
  list = [1, 2, 3]

  num_str = provider::pyvider::tostring(local.number)  # "42"
  bool_str = provider::pyvider::tostring(local.basic_boolean)  # "true"
  list_str = provider::pyvider::tostring(local.list)  # "[1, 2, 3]"
}

output "basic_boolean" {
  value = {
    number = local.num_str
    boolean = local.bool_str
    list = local.list_str
  }
}
