locals {
  to_camel_case_text = "hello_world"
  camel = provider::pyvider::to_camel_case(local.to_camel_case_text)
  # "helloWorld"
  pascal = provider::pyvider::to_camel_case(local.to_camel_case_text, true)
  # "HelloWorld"
}

output "to_camel_case_text" {
  value = {
    camel  = local.camel
    pascal = local.pascal
  }
}
