locals {
  tostring_tostring_integer = 42
  tostring_tostring_float   = 3.14159
  tostring_tostring_boolean = true

  tostring_tostring_int_string   = provider::pyvider::tostring(local.tostring_tostring_integer)  # "42"
  tostring_tostring_float_string = provider::pyvider::tostring(local.tostring_tostring_float)    # "3.14159"
  tostring_bool_string  = provider::pyvider::tostring(local.tostring_tostring_boolean)  # "true"
}

output "tostring_tostring_boolean" {
  value = {
    integer = local.tostring_tostring_int_string
    float   = local.tostring_tostring_float_string
    boolean = local.tostring_bool_string
  }
}
