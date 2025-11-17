locals {
  text = "HelloWorld"
  kebab = provider::pyvider::to_kebab_case(local.text)
  # "hello-world"
}

output "to_kebab_case_example" {
  value = local.kebab
}
