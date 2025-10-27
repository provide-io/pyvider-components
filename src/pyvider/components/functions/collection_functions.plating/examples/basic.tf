# Basic collection operations
locals {
  items = ["apple", "banana", "cherry"]
  config = { host = "localhost", port = 8080 }

  count = provider::pyvider::length(local.items)  # 3
  has_apple = provider::pyvider::contains(local.items, "apple")  # true
  port = provider::pyvider::lookup(local.config, "port", 3000)  # 8080
}

output "basic_collections" {
  value = {
    count = local.count
    has_apple = local.has_apple
    port = local.port
  }
}
