locals {
  to_snake_case_text = "HelloWorld"
  snake = provider::pyvider::to_snake_case(local.to_snake_case_text)
  # "hello_world"
}

output "to_snake_case_text" {
  value = local.snake
}
