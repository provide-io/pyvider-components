# Basic collection function examples

# Example 1: Length function
locals {
  comp_numbers = [1, 2, 3, 4, 5]
  comp_colors  = ["red", "green", "blue"]
  comp_message = "Hello World"
  comp_config  = { host = "localhost", port = 8080 }

  numbers_length = provider::pyvider::length(local.comp_numbers) # 5
  colors_length  = provider::pyvider::length(local.comp_colors)  # 3
  message_length = provider::pyvider::length(local.comp_message) # 11
  config_length  = provider::pyvider::length(local.comp_config)  # 2
}

# Example 2: Contains function
locals {
  comp_fruits = ["apple", "banana", "cherry"]
  comp_ports  = [80, 443, 8080]

  comp_has_apple  = provider::pyvider::contains(local.comp_fruits, "apple")  # true
  comp_has_grape  = provider::pyvider::contains(local.comp_fruits, "grape")  # false
  comp_has_port80 = provider::pyvider::contains(local.comp_ports, 80)        # true
  comp_has_port22 = provider::pyvider::contains(local.comp_ports, 22)        # false
}

# Example 3: Lookup function
locals {
  comp_settings = {
    comp_database_host = "db.example.com"
    comp_database_port = 5432
    comp_cache_host    = "redis.local"
  }

  db_host      = provider::pyvider::lookup(local.comp_settings, "database_host", "localhost")
  db_port      = provider::pyvider::lookup(local.comp_settings, "database_port", 5432)
  unknown_key  = provider::pyvider::lookup(local.comp_settings, "missing_key", "default")
}

# Example 4: Practical usage
locals {
  comp_servers = ["web1", "web2", "web3"]

  comp_server_count   = provider::pyvider::length(local.comp_servers)
  comp_has_web1       = provider::pyvider::contains(local.comp_servers, "web1")
  comp_needs_scaling  = local.comp_server_count < 5
}

output "collection_examples" {
  value = {
    lengths = {
      numbers = local.numbers_length
      colors  = local.colors_length
      message = local.message_length
      config  = local.config_length
    }
    contains_checks = {
      has_apple  = local.comp_has_apple
      has_grape  = local.comp_has_grape
      has_port80 = local.comp_has_port80
    }
    lookups = {
      db_host     = local.db_host
      db_port     = local.db_port
      unknown_key = local.unknown_key
    }
    practical = {
      server_count  = local.comp_server_count
      has_web1      = local.comp_has_web1
      needs_scaling = local.comp_needs_scaling
    }
  }
}
