locals {
  contains_contains_fruits = ["apple", "banana", "cherry"]
  contains_contains_has_apple = provider::pyvider::contains(local.contains_contains_fruits, "apple")   # true
  contains_contains_has_grape = provider::pyvider::contains(local.contains_contains_fruits, "grape")   # false
}

output "contains_contains_has_grape" {
  value = {
    has_apple = local.contains_contains_has_apple
    has_grape = local.contains_contains_has_grape
  }
}
