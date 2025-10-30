locals {
  join_words = ["apple", "banana", "cherry"]
  join_joined = provider::pyvider::join(local.join_words, ", ")
  # "apple, banana, cherry"
}

output "join_example" {
  value = local.join_joined
}
