locals {
  to_camel_case_text = "hello_world"
  to_camel_case_camel = provider::pyvider::to_camel_case(local.to_camel_case_text)
  # "helloWorld"
  to_camel_case_pascal = provider::pyvider::to_camel_case(local.to_camel_case_text, true)
  # "HelloWorld"
}

output "to_camel_case_example" {
  value = {
    camel  = local.to_camel_case_camel
    pascal = local.to_camel_case_pascal
  }
}
