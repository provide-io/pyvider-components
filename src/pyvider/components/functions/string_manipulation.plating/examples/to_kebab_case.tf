locals {
  to_kebab_case_text = "HelloWorld"
  kebab = provider::pyvider::to_kebab_case(local.to_kebab_case_text)
  # "hello-world"
}

output "to_kebab_case_text" {
  value = local.kebab
}
