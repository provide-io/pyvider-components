# Advanced collection operations

# Cascading defaults with lookup
locals {
  user_config = {
    theme = "dark"
    language = "en"
  }

  default_config = {
    theme = "light"
    language = "en"
    timezone = "UTC"
    notifications = true
  }

  # Lookup with cascading defaults
  final_theme = provider::pyvider::lookup(
    local.user_config,
    "theme",
    provider::pyvider::lookup(local.default_config, "theme", "light")
  )

  final_timezone = provider::pyvider::lookup(
    local.user_config,
    "timezone",
    provider::pyvider::lookup(local.default_config, "timezone", "UTC")
  )
}

# Feature flag checking
locals {
  enabled_features = ["api_v2", "new_ui", "advanced_search"]

  # Check if features are enabled
  api_v2_enabled = provider::pyvider::contains(local.enabled_features, "api_v2")
  beta_enabled = provider::pyvider::contains(local.enabled_features, "beta_features")

  # Conditional logic based on contains
  api_endpoint = local.api_v2_enabled ? "/api/v2" : "/api/v1"
}

# Length-based conditional logic
locals {
  validation_errors = []  # Would be populated by validation

  has_errors = provider::pyvider::length(local.validation_errors) > 0
  error_count = provider::pyvider::length(local.validation_errors)

  status = local.has_errors ? "invalid" : "valid"
}

# Nested map lookups
locals {
  config_tree = {
    database = {
      primary = {
        host = "db1.example.com"
        port = 5432
      }
      replica = {
        host = "db2.example.com"
        port = 5432
      }
    }
    cache = {
      redis = {
        host = "redis.example.com"
        port = 6379
      }
    }
  }

  # Safe nested lookups
  db_config = provider::pyvider::lookup(local.config_tree, "database", {})
  primary_db = provider::pyvider::lookup(local.db_config, "primary", {})
  db_host = provider::pyvider::lookup(local.primary_db, "host", "localhost")
}

# Collection size validation
locals {
  required_fields = ["name", "email", "role"]
  provided_fields = ["name", "email"]

  all_required_present = provider::pyvider::length(local.required_fields) == provider::pyvider::length([
    for field in local.required_fields :
    field if provider::pyvider::contains(local.provided_fields, field)
  ])
}

output "advanced_collection_results" {
  value = {
    configuration = {
      theme = local.final_theme
      timezone = local.final_timezone
    }
    features = {
      api_v2 = local.api_v2_enabled
      beta = local.beta_enabled
      endpoint = local.api_endpoint
    }
    validation = {
      has_errors = local.has_errors
      error_count = local.error_count
      status = local.status
      all_required = local.all_required_present
    }
    nested_config = {
      db_host = local.db_host
    }
  }
}
