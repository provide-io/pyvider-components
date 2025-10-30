# Basic collection operations
locals {
  basic_items = ["apple", "banana", "cherry"]
  basic_basic_config = { host = "localhost", port = 8080 }

  count = provider::pyvider::length(local.basic_items)  # 3
  has_apple = provider::pyvider::contains(local.basic_items, "apple")  # true
  port = provider::pyvider::lookup(local.basic_basic_config, "port", 3000)  # 8080
}

output "basic_basic_config" {
  value = {
    count = local.count
    has_apple = local.has_apple
    port = local.port
  }
}
