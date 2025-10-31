locals {
  words = ["apple", "banana", "cherry"]
  joined = provider::pyvider::join(local.words, ", ")
  # "apple, banana, cherry"
}

output "join_example" {
  value = local.joined
}
