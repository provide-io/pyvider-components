locals {
  integer = 42
  float   = 3.14159
  boolean = true

  int_string   = provider::pyvider::tostring(local.integer)  # "42"
  float_string = provider::pyvider::tostring(local.float)    # "3.14159"
  bool_string  = provider::pyvider::tostring(local.boolean)  # "true"
}

output "tostring_example" {
  value = {
    integer = local.int_string
    float   = local.float_string
    boolean = local.bool_string
  }
}
