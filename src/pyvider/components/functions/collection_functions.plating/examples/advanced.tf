# Advanced collection operations

# Cascading defaults with lookup
locals {
  advanced_user_config = {
    advanced_theme = "dark"
    advanced_language = "en"
  }

  default_config = {
    theme = "light"
    language = "en"
    timezone = "UTC"
    notifications = true
  }

  # Lookup with cascading defaults
  final_theme = provider::pyvider::lookup(
    local.advanced_user_config,
    "theme",
    provider::pyvider::lookup(local.default_config, "theme", "light")
  )

  final_timezone = provider::pyvider::lookup(
    local.advanced_user_config,
    "timezone",
    provider::pyvider::lookup(local.default_config, "timezone", "UTC")
  )
}

# Feature flag checking
locals {
  advanced_enabled_features = ["api_v2", "new_ui", "advanced_search"]

  # Check if features are enabled
  advanced_api_v2_enabled = provider::pyvider::contains(local.advanced_enabled_features, "api_v2")
  advanced_beta_enabled = provider::pyvider::contains(local.advanced_enabled_features, "beta_features")

  # Conditional logic based on contains
  advanced_api_endpoint = local.advanced_api_v2_enabled ? "/api/v2" : "/api/v1"
}

# Length-based conditional logic
locals {
  advanced_validation_errors = []  # Would be populated by validation

  advanced_has_errors = provider::pyvider::length(local.advanced_validation_errors) > 0
  advanced_error_count = provider::pyvider::length(local.advanced_validation_errors)

  advanced_status = local.advanced_has_errors ? "invalid" : "valid"
}

# Nested map lookups
locals {
  advanced_config_tree = {
    advanced_database = {
      advanced_primary = {
        advanced_host = "db1.example.com"
        advanced_port = 5432
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
  db_config = provider::pyvider::lookup(local.advanced_config_tree, "database", {})
  primary_db = provider::pyvider::lookup(local.db_config, "primary", {})
  db_host = provider::pyvider::lookup(local.primary_db, "host", "localhost")
}

# Collection size validation
locals {
  advanced_required_fields = ["name", "email", "role"]
  advanced_provided_fields = ["name", "email"]

  advanced_all_required_present = provider::pyvider::length(local.advanced_required_fields) == provider::pyvider::length([
    for field in local.advanced_required_fields :
    field if provider::pyvider::contains(local.advanced_provided_fields, field)
  ])
}

output "advanced_error_count" {
  value = {
    configuration = {
      theme = local.final_theme
      timezone = local.final_timezone
    }
    features = {
      api_v2 = local.advanced_api_v2_enabled
      beta = local.advanced_beta_enabled
      endpoint = local.advanced_api_endpoint
    }
    validation = {
      has_errors = local.advanced_has_errors
      error_count = local.advanced_error_count
      status = local.advanced_status
      all_required = local.advanced_all_required_present
    }
    nested_config = {
      db_host = local.db_host
    }
  }
}
