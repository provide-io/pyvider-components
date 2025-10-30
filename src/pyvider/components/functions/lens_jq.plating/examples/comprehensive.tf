# Basic lens_jq function examples

# Example 1: Simple field extraction
locals {
  comp_user_data = {
    id    = 123
    comp_name  = "Alice Johnson"
    comp_email = "alice@example.com"
  }

  user_name  = provider::pyvider::lens_jq(local.comp_user_data, ".name")
  user_email = provider::pyvider::lens_jq(local.comp_user_data, ".email")
  user_id    = provider::pyvider::lens_jq(local.comp_user_data, ".id")
}

# Example 2: Array operations
locals {
  comp_colors = ["red", "green", "blue", "yellow"]

  comp_first_color = provider::pyvider::lens_jq(local.comp_colors, ".[0]")
  comp_last_color  = provider::pyvider::lens_jq(local.comp_colors, ".[-1]")
  comp_color_count = provider::pyvider::lens_jq(local.comp_colors, "length")
}

# Example 3: Nested field access
locals {
  comp_config = {
    comp_database = {
      comp_host = "localhost"
      comp_port = 5432
    }
    cache = {
      host = "redis.local"
      port = 6379
    }
  }

  db_host    = provider::pyvider::lens_jq(local.comp_config, ".database.host")
  db_port    = provider::pyvider::lens_jq(local.comp_config, ".database.port")
  cache_host = provider::pyvider::lens_jq(local.comp_config, ".cache.host")
}

# Example 4: Simple data transformation
locals {
  comp_users = [
    { name = "Alice", active = true },
    { name = "Bob", active = false },
    { name = "Carol", active = true }
  ]

  active_users = provider::pyvider::lens_jq(local.comp_users, "map(select(.active == true))")
  user_names   = provider::pyvider::lens_jq(local.comp_users, "map(.name)")
}

# Output the results
output "lens_jq_examples" {
  value = {
    user_extraction = {
      name  = local.user_name
      email = local.user_email
      id    = local.user_id
    }
    array_operations = {
      first = local.comp_first_color
      last  = local.comp_last_color
      count = local.comp_color_count
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
