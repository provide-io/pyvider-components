locals {
  item = "apple"
  singular = provider::pyvider::pluralize(local.item, 1)  # "apple"
  plural = provider::pyvider::pluralize(local.item, 2)    # "apples"
  custom = provider::pyvider::pluralize("person", 2, "people")  # "people"
}

output "pluralize_example" {
  value = {
    singular = local.singular
    plural   = local.plural
    custom   = local.custom
  }
}
