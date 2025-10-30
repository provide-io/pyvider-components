locals {
  replace_text = "hello world"
  replaced = provider::pyvider::replace(local.replace_text, "world", "earth")
  # "hello earth"
}

output "replace_text" {
  value = local.replaced
}
