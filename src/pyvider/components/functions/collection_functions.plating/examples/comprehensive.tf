# Basic collection function examples

# Example 1: Length function
locals {
  comprehensive_comprehensive_numbers = [1, 2, 3, 4, 5]
  comprehensive_colors  = ["red", "green", "blue"]
  comprehensive_message = "Hello World"
  comprehensive_comprehensive_config  = { host = "localhost", port = 8080 }

  numbers_length = provider::pyvider::length(local.comprehensive_comprehensive_numbers) # 5
  colors_length  = provider::pyvider::length(local.comprehensive_colors)  # 3
  message_length = provider::pyvider::length(local.comprehensive_message) # 11
  config_length  = provider::pyvider::length(local.comprehensive_comprehensive_config)  # 2
}

# Example 2: Contains function
locals {
  comprehensive_comprehensive_fruits = ["apple", "banana", "cherry"]
  comprehensive_ports  = [80, 443, 8080]

  comprehensive_comprehensive_has_apple  = provider::pyvider::contains(local.comprehensive_comprehensive_fruits, "apple")  # true
  comprehensive_comprehensive_has_grape  = provider::pyvider::contains(local.comprehensive_comprehensive_fruits, "grape")  # false
  comprehensive_has_port80 = provider::pyvider::contains(local.comprehensive_ports, 80)        # true
  comprehensive_has_port22 = provider::pyvider::contains(local.comprehensive_ports, 22)        # false
}

# Example 3: Lookup function
locals {
  comprehensive_comprehensive_settings = {
    comprehensive_comprehensive_database_host = "db.example.com"
    comprehensive_comprehensive_database_port = 5432
    comprehensive_cache_host    = "redis.local"
  }

  db_host      = provider::pyvider::lookup(local.comprehensive_comprehensive_settings, "database_host", "localhost")
  db_port      = provider::pyvider::lookup(local.comprehensive_comprehensive_settings, "database_port", 5432)
  unknown_key  = provider::pyvider::lookup(local.comprehensive_comprehensive_settings, "missing_key", "default")
}

# Example 4: Practical usage
locals {
  comprehensive_servers = ["web1", "web2", "web3"]

  comprehensive_server_count   = provider::pyvider::length(local.comprehensive_servers)
  comprehensive_has_web1       = provider::pyvider::contains(local.comprehensive_servers, "web1")
  comprehensive_needs_scaling  = local.comprehensive_server_count < 5
}

output "comprehensive_comprehensive_settings" {
  value = {
    lengths = {
      numbers = local.numbers_length
      colors  = local.colors_length
      message = local.message_length
      config  = local.config_length
    }
    contains_checks = {
      has_apple  = local.comprehensive_comprehensive_has_apple
      has_grape  = local.comprehensive_comprehensive_has_grape
      has_port80 = local.comprehensive_has_port80
    }
    lookups = {
      db_host     = local.db_host
      db_port     = local.db_port
      unknown_key = local.unknown_key
    }
    practical = {
      server_count  = local.comprehensive_server_count
      has_web1      = local.comprehensive_has_web1
      needs_scaling = local.comprehensive_needs_scaling
    }
  }
}
