locals {
  shout = provider::pyvider::upper("hello world") # "HELLO WORLD"
}

output "upper_example" {
  value = local.shout
}
