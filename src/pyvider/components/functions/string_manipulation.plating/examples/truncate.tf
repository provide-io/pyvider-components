locals {
  truncate_text = "Very long text that needs truncation"
  truncated = provider::pyvider::truncate(local.truncate_text, 10)  # "Very lo..."
  custom_suffix = provider::pyvider::truncate(local.truncate_text, 10, ">>")  # "Very long>>"
}

output "truncate_text" {
  value = {
    default = local.truncated
    custom  = local.custom_suffix
  }
}
