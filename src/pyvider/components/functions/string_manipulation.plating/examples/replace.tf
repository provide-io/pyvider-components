locals {
  text = "hello world"
  replaced = provider::pyvider::replace(local.text, "world", "earth")
  # "hello earth"
}

output "replace_example" {
  value = local.replaced
}
