# Basic type conversion
locals {
  number = 42
  boolean = true
  list = [1, 2, 3]

  num_str = provider::pyvider::tostring(local.number)  # "42"
  bool_str = provider::pyvider::tostring(local.boolean)  # "true"
  list_str = provider::pyvider::tostring(local.list)  # "[1, 2, 3]"
}

output "basic_conversion" {
  value = {
    number = local.num_str
    boolean = local.bool_str
    list = local.list_str
  }
}
