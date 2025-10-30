locals {
  fruits = ["apple", "banana", "cherry"]
  has_apple = provider::pyvider::contains(local.fruits, "apple")   # true
  has_grape = provider::pyvider::contains(local.fruits, "grape")   # false
}

output "contains_example" {
  value = {
    has_apple = local.has_apple
    has_grape = local.has_grape
  }
}
