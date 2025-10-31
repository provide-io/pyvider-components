locals {
  text = "Very long text that needs truncation"
  truncated = provider::pyvider::truncate(local.text, 10)  # "Very lo..."
  custom_suffix = provider::pyvider::truncate(local.text, 10, ">>")  # "Very long>>"
}

output "truncate_example" {
  value = {
    default = local.truncated
    custom  = local.custom_suffix
  }
}
