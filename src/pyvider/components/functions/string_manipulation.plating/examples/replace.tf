locals {
  replace_text = "hello world"
  replace_replaced = provider::pyvider::replace(local.replace_text, "world", "earth")
  # "hello earth"
}

output "replace_example" {
  value = local.replace_replaced
}
