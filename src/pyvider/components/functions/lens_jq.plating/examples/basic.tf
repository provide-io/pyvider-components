# Basic jq operations
locals {
  basic_data = {
    user = { name = "Alice", age = 30 }
    items = ["one", "two", "three"]
  }

  user_name = provider::pyvider::lens_jq(local.basic_data, ".user.name")  # "Alice"
  item_count = provider::pyvider::lens_jq(local.basic_data, ".items | length")  # 3
  first_item = provider::pyvider::lens_jq(local.basic_data, ".items[0]")  # "one"
}

output "basic_data" {
  value = {
    name = local.user_name
    count = local.item_count
    first = local.first_item
  }
}
