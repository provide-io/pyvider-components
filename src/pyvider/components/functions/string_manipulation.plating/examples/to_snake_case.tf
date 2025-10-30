locals {
  to_snake_case_text = "HelloWorld"
  to_snake_case_snake = provider::pyvider::to_snake_case(local.to_snake_case_text)
  # "hello_world"
}

output "to_snake_case_example" {
  value = local.to_snake_case_snake
}
