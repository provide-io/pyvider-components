locals {
  text = "hello_world"
  camel = provider::pyvider::to_camel_case(local.text)
  # "helloWorld"
  pascal = provider::pyvider::to_camel_case(local.text, true)
  # "HelloWorld"
}

output "to_camel_case_example" {
  value = {
    camel  = local.camel
    pascal = local.pascal
  }
}
