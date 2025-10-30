locals {
  default_display = provider::pyvider::format_size(10240)        # "10.0 KB"
  precise_display = provider::pyvider::format_size(123456789, 2) # "117.74 MB"
}

output "format_size_example" {
  value = {
    default = local.default_display
    precise = local.precise_display
  }
}
