# Basic jq operations
locals {
  basic_data = {
    user = { name = "Alice", age = 30 }
    items = ["one", "two", "three"]
  }

  basic_user_name = provider::pyvider::lens_jq(local.basic_data, ".user.name")  # "Alice"
  basic_item_count = provider::pyvider::lens_jq(local.basic_data, ".items | length")  # 3
  basic_first_item = provider::pyvider::lens_jq(local.basic_data, ".items[0]")  # "one"
}

output "basic_jq" {
  value = {
    name = local.basic_user_name
    count = local.basic_item_count
    first = local.basic_first_item
  }
}
