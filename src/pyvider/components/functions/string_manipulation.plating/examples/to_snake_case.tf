locals {
  text = "HelloWorld"
  snake = provider::pyvider::to_snake_case(local.text)
  # "hello_world"
}

output "to_snake_case_example" {
  value = local.snake
}
