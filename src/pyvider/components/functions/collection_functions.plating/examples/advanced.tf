# Advanced collection operations

# Cascading defaults with lookup
locals {
  adv_user_config = {
    adv_theme = "dark"
    adv_language = "en"
  }

  default_config = {
    theme = "light"
    language = "en"
    timezone = "UTC"
    notifications = true
  }

  # Lookup with cascading defaults
  final_theme = provider::pyvider::lookup(
    local.adv_user_config,
    "theme",
    provider::pyvider::lookup(local.default_config, "theme", "light")
  )

  final_timezone = provider::pyvider::lookup(
    local.adv_user_config,
    "timezone",
    provider::pyvider::lookup(local.default_config, "timezone", "UTC")
  )
}

# Feature flag checking
locals {
  adv_enabled_features = ["api_v2", "new_ui", "advanced_search"]

  # Check if features are enabled
  adv_api_v2_enabled = provider::pyvider::contains(local.adv_enabled_features, "api_v2")
  adv_beta_enabled = provider::pyvider::contains(local.adv_enabled_features, "beta_features")

  # Conditional logic based on contains
  adv_api_endpoint = local.adv_api_v2_enabled ? "/api/v2" : "/api/v1"
}

# Length-based conditional logic
locals {
  adv_validation_errors = []  # Would be populated by validation

  adv_has_errors = provider::pyvider::length(local.adv_validation_errors) > 0
  adv_error_count = provider::pyvider::length(local.adv_validation_errors)

  status = local.adv_has_errors ? "invalid" : "valid"
}

# Nested map lookups
locals {
  adv_config_tree = {
    adv_database = {
      adv_primary = {
        adv_host = "db1.example.com"
        adv_port = 5432
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
  db_config = provider::pyvider::lookup(local.adv_config_tree, "database", {})
  primary_db = provider::pyvider::lookup(local.db_config, "primary", {})
  db_host = provider::pyvider::lookup(local.primary_db, "host", "localhost")
}

# Collection size validation
locals {
  adv_required_fields = ["name", "email", "role"]
  adv_provided_fields = ["name", "email"]

  adv_all_required_present = provider::pyvider::length(local.adv_required_fields) == provider::pyvider::length([
    for field in local.adv_required_fields :
    field if provider::pyvider::contains(local.adv_provided_fields, field)
  ])
}

output "advanced_collection_results" {
  value = {
    configuration = {
      theme = local.final_theme
      timezone = local.final_timezone
    }
    features = {
      api_v2 = local.adv_api_v2_enabled
      beta = local.adv_beta_enabled
      endpoint = local.adv_api_endpoint
    }
    validation = {
      has_errors = local.adv_has_errors
      error_count = local.adv_error_count
      status = local.status
      all_required = local.adv_all_required_present
    }
    nested_config = {
      db_host = local.db_host
    }
  }
}
