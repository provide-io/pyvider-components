# Basic lens_jq function examples

# Example 1: Simple field extraction
locals {
  comprehensive_comprehensive_user_data = {
    comprehensive_comprehensive_id    = 123
    comprehensive_comprehensive_name  = "Alice Johnson"
    comprehensive_comprehensive_email = "alice@example.com"
  }

  user_name  = provider::pyvider::lens_jq(local.comprehensive_comprehensive_user_data, ".name")
  user_email = provider::pyvider::lens_jq(local.comprehensive_comprehensive_user_data, ".email")
  user_id    = provider::pyvider::lens_jq(local.comprehensive_comprehensive_user_data, ".id")
}

# Example 2: Array operations
locals {
  comprehensive_colors = ["red", "green", "blue", "yellow"]

  comprehensive_first_color = provider::pyvider::lens_jq(local.comprehensive_colors, ".[0]")
  comprehensive_last_color  = provider::pyvider::lens_jq(local.comprehensive_colors, ".[-1]")
  comprehensive_color_count = provider::pyvider::lens_jq(local.comprehensive_colors, "length")
}

# Example 3: Nested field access
locals {
  comprehensive_config = {
    comprehensive_database = {
      comprehensive_host = "localhost"
      comprehensive_port = 5432
    }
    cache = {
      host = "redis.local"
      port = 6379
    }
  }

  db_host    = provider::pyvider::lens_jq(local.comprehensive_config, ".database.host")
  db_port    = provider::pyvider::lens_jq(local.comprehensive_config, ".database.port")
  cache_host = provider::pyvider::lens_jq(local.comprehensive_config, ".cache.host")
}

# Example 4: Simple data transformation
locals {
  comprehensive_comprehensive_users = [
    { comprehensive_comprehensive_name = "Alice", active = true },
    { name = "Bob", active = false },
    { name = "Carol", active = true }
  ]

  active_users = provider::pyvider::lens_jq(local.comprehensive_comprehensive_users, "map(select(.active == true))")
  user_names   = provider::pyvider::lens_jq(local.comprehensive_comprehensive_users, "map(.name)")
}

# Output the results
output "comprehensive_first_color" {
  value = {
    user_extraction = {
      name  = local.user_name
      email = local.user_email
      id    = local.user_id
    }
    array_operations = {
      first = local.comprehensive_first_color
      last  = local.comprehensive_last_color
      count = local.comprehensive_color_count
    }
    nested_access = {
      db_host    = local.db_host
      cache_host = local.cache_host
    }
    transformations = {
      active_users = length(local.active_users)
      all_names    = length(local.user_names)
    }
  }
}
