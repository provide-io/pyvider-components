---
page_title: "Function: lower"
description: |-
  Converts a string to lowercase with null-safe handling
---

# lower (Function)

> Converts all characters in a string to lowercase with null-safe handling

The `lower` function takes a string and returns a new string with all alphabetic characters converted to lowercase. It handles null values gracefully by returning null when the input is null.

## When to Use This

- **Case normalization**: Standardize text case for comparisons
- **URL/path formatting**: Format paths and URLs consistently
- **Data consistency**: Normalize user input or imported data
- **File naming**: Create consistent lowercase filenames
- **Search operations**: Normalize text for case-insensitive matching

**Anti-patterns (when NOT to use):**
- Preserving original case formatting (use original string)
- Binary data or non-text content
- When case sensitivity is required
- Proper nouns that should maintain capitalization

## Quick Start

```terraform
# Simple case conversion
locals {
  service_name = "USER-SERVICE"
  service_lower = provider::pyvider::lower(local.service_name)  # Returns: "user-service"
}

# File naming
variable "component_name" {
  default = "DataProcessor"
}

locals {
  filename = "${provider::pyvider::lower(var.component_name)}.conf"  # Returns: "dataprocessor.conf"
}
```

## Examples

### Basic Usage

```terraform
# Simple case conversion
locals {
  basic_examples = {
    simple_text = provider::pyvider::lower("Hello World")           # "hello world"
    mixed_case = provider::pyvider::lower("MiXeD cAsE")            # "mixed case"
    already_lower = provider::pyvider::lower("already lowercase")   # "already lowercase"
    with_numbers = provider::pyvider::lower("Test123")              # "test123"
    special_chars = provider::pyvider::lower("Hello@World.com")     # "hello@world.com"
    empty_string = provider::pyvider::lower("")                     # ""
  }

  # Working with variables
  service_name = "USER-AUTHENTICATION-SERVICE"
  normalized_service = provider::pyvider::lower(local.service_name)  # "user-authentication-service"

  # Handling null values
  null_input = null
  null_result = provider::pyvider::lower(local.null_input)  # null

  # Lists and collections
  mixed_case_list = ["FIRST", "Second", "tHiRd", "FOURTH"]
  lowercase_list = [
    for item in local.mixed_case_list :
    provider::pyvider::lower(item)
  ]
  # Result: ["first", "second", "third", "fourth"]
}

# Conditional case conversion
variable "preserve_case" {
  type    = bool
  default = false
}

locals {
  original_text = "System Configuration"
  processed_text = var.preserve_case ? local.original_text : provider::pyvider::lower(local.original_text)
}

output "basic_lower_examples" {
  value = {
    examples = local.basic_examples
    service_normalized = local.normalized_service
    list_conversion = local.lowercase_list
    conditional_result = local.processed_text
  }
}
```

### Configuration and Environment Management

```terraform
# Environment variable normalization
variable "environment_configs" {
  type = map(object({
    database_host = string
    cache_server = string
    log_level = string
    app_mode = string
  }))
  default = {
    PRODUCTION = {
      database_host = "PROD-DB.COMPANY.COM"
      cache_server = "PROD-CACHE-01.INTERNAL"
      log_level = "ERROR"
      app_mode = "PRODUCTION"
    }
    STAGING = {
      database_host = "STAGING-DB.COMPANY.COM"
      cache_server = "STAGING-CACHE.INTERNAL"
      log_level = "DEBUG"
      app_mode = "STAGING"
    }
    DEVELOPMENT = {
      database_host = "localhost"
      cache_server = "LOCAL-CACHE"
      log_level = "DEBUG"
      app_mode = "DEVELOPMENT"
    }
  }
}

# Normalize configuration values for consistency
locals {
  normalized_configs = {
    for env_name, config in var.environment_configs :
    provider::pyvider::lower(env_name) => {
      # Normalize database host for connection strings
      database_host = provider::pyvider::lower(config.database_host)
      cache_server = provider::pyvider::lower(config.cache_server)

      # Normalize log level for consistent logging configuration
      log_level = provider::pyvider::lower(config.log_level)

      # Keep app mode normalized for environment detection
      app_mode = provider::pyvider::lower(config.app_mode)

      # Generate environment-specific configuration keys
      config_prefix = "app_${provider::pyvider::lower(env_name)}"

      # Create connection strings with normalized hostnames
      database_url = "postgresql://user:pass@${provider::pyvider::lower(config.database_host)}:5432/myapp"
      cache_url = "redis://${provider::pyvider::lower(config.cache_server)}:6379/0"

      # Environment detection helpers
      is_production = provider::pyvider::lower(config.app_mode) == "production"
      is_development = provider::pyvider::lower(config.app_mode) == "development"
    }
  }

  # Generate environment-specific configuration files
  config_files = {
    for env_name, config in local.normalized_configs :
    env_name => {
      filename = "${config.config_prefix}.conf"
      content = join("\n", [
        "# ${title(env_name)} Environment Configuration",
        "database_host=${config.database_host}",
        "cache_server=${config.cache_server}",
        "log_level=${config.log_level}",
        "app_mode=${config.app_mode}",
        "database_url=${config.database_url}",
        "cache_url=${config.cache_url}"
      ])
    }
  }

  # Generate Docker Compose service names (must be lowercase)
  docker_services = {
    for env_name, config in local.normalized_configs :
    env_name => {
      app_service = "app-${env_name}"
      db_service = "db-${env_name}"
      cache_service = "cache-${env_name}"

      # Docker Compose configuration
      compose_config = {
        version = "3.8"
        services = {
          "${local.docker_services[env_name].app_service}" = {
            image = "myapp:latest"
            environment = {
              DATABASE_URL = config.database_url
              CACHE_URL = config.cache_url
              LOG_LEVEL = config.log_level
              APP_MODE = config.app_mode
            }
          }
        }
      }
    }
  }
}

output "configuration_management" {
  value = {
    normalized_configs = local.normalized_configs
    config_files = local.config_files
    docker_services = local.docker_services
  }
}
```

### Search and Indexing Operations

```terraform
# Search index normalization
variable "search_documents" {
  type = list(object({
    title = string
    content = string
    tags = list(string)
    category = string
    author = string
  }))
  default = [
    {
      title = "Getting Started with Terraform"
      content = "Terraform is an Infrastructure as Code Tool that allows you to manage cloud resources declaratively."
      tags = ["Infrastructure", "Cloud", "DevOps", "Automation"]
      category = "Tutorial"
      author = "John Smith"
    },
    {
      title = "Advanced Kubernetes Patterns"
      content = "Learn advanced deployment patterns for Kubernetes including Blue-Green deployments and Canary releases."
      tags = ["Kubernetes", "Deployment", "Patterns", "Advanced"]
      category = "Advanced Guide"
      author = "Jane DOE"
    },
    {
      title = "Database Migration Best Practices"
      content = "Best practices for managing database schema changes and migrations in production environments."
      tags = ["Database", "Migration", "Production", "Schema"]
      category = "Best Practices"
      author = "Mike JOHNSON"
    }
  ]
}

# Create search-friendly normalized documents
locals {
  search_index = {
    for idx, doc in var.search_documents :
    idx => {
      # Normalize all text fields for case-insensitive searching
      title_normalized = provider::pyvider::lower(doc.title)
      content_normalized = provider::pyvider::lower(doc.content)
      author_normalized = provider::pyvider::lower(doc.author)
      category_normalized = provider::pyvider::lower(doc.category)

      # Normalize tags for consistent tagging
      tags_normalized = [
        for tag in doc.tags :
        provider::pyvider::lower(tag)
      ]

      # Create searchable text blob
      searchable_text = provider::pyvider::lower("${doc.title} ${doc.content} ${join(" ", doc.tags)} ${doc.category} ${doc.author}")

      # Generate search keywords
      keywords = distinct([
        provider::pyvider::lower(doc.title),
        provider::pyvider::lower(doc.category),
        provider::pyvider::lower(doc.author)
      ])

      # Create URL-friendly slugs
      title_slug = replace(
        replace(
          provider::pyvider::lower(doc.title),
          " ", "-"
        ),
        "[^a-z0-9-]", ""
      )

      # Original document for display
      original = doc
    }
  }

  # Build search functionality
  search_functions = {
    # Function to search by title
    search_by_title = {
      for term in ["terraform", "kubernetes", "database"] :
      term => [
        for idx, doc in local.search_index :
        doc if contains(split(" ", doc.title_normalized), term)
      ]
    }

    # Function to search by category
    search_by_category = {
      for category in distinct([for doc in local.search_index : doc.category_normalized]) :
      category => [
        for idx, doc in local.search_index :
        doc if doc.category_normalized == category
      ]
    }

    # Function to search by tags
    search_by_tags = {
      for tag in distinct(flatten([for doc in local.search_index : doc.tags_normalized])) :
      tag => [
        for idx, doc in local.search_index :
        doc if contains(doc.tags_normalized, tag)
      ]
    }
  }

  # Auto-complete suggestions (lowercase for consistency)
  autocomplete_suggestions = distinct(concat(
    [for doc in local.search_index : doc.title_normalized],
    [for doc in local.search_index : doc.category_normalized],
    [for doc in local.search_index : doc.author_normalized],
    flatten([for doc in local.search_index : doc.tags_normalized])
  ))
}

output "search_indexing" {
  value = {
    search_index = local.search_index
    search_functions = local.search_functions
    autocomplete = local.autocomplete_suggestions
  }
}
```

### System Integration and API Keys

```terraform
# API key and identifier normalization
variable "system_integrations" {
  type = map(object({
    service_name = string
    api_endpoints = list(string)
    authentication_type = string
    environment_variables = map(string)
    configuration_keys = list(string)
  }))
  default = {
    payment_gateway = {
      service_name = "PaymentGateway-API"
      api_endpoints = [
        "https://API.PaymentGateway.COM/v1/payments",
        "https://API.PaymentGateway.COM/v1/refunds"
      ]
      authentication_type = "API-KEY"
      environment_variables = {
        "PAYMENT_API_KEY" = "key_12345"
        "PAYMENT_SECRET" = "secret_67890"
        "PAYMENT_ENDPOINT" = "https://API.PaymentGateway.COM"
      }
      configuration_keys = ["payment.api.key", "payment.secret", "payment.endpoint"]
    }
    notification_service = {
      service_name = "NotificationHub"
      api_endpoints = [
        "https://NOTIFICATIONS.SERVICE.COM/send",
        "https://NOTIFICATIONS.SERVICE.COM/status"
      ]
      authentication_type = "BEARER-TOKEN"
      environment_variables = {
        "NOTIFICATION_TOKEN" = "token_abcdef"
        "NOTIFICATION_URL" = "https://NOTIFICATIONS.SERVICE.COM"
      }
      configuration_keys = ["notification.token", "notification.url"]
    }
  }
}

# Normalize system integration configurations
locals {
  normalized_integrations = {
    for integration_name, config in var.system_integrations :
    provider::pyvider::lower(integration_name) => {
      # Normalize service identifiers
      service_name = provider::pyvider::lower(config.service_name)
      auth_type = provider::pyvider::lower(config.authentication_type)

      # Normalize API endpoints (convert to lowercase for consistency)
      api_endpoints = [
        for endpoint in config.api_endpoints :
        provider::pyvider::lower(endpoint)
      ]

      # Normalize environment variable names (typically uppercase, but values lowercase)
      environment_variables = {
        for key, value in config.environment_variables :
        key => provider::pyvider::lower(value)
      }

      # Normalize configuration keys
      configuration_keys = [
        for key in config.configuration_keys :
        provider::pyvider::lower(key)
      ]

      # Generate service-specific configuration
      service_config = {
        # Connection configuration
        connection_name = "conn_${provider::pyvider::lower(integration_name)}"
        client_id = "client_${provider::pyvider::lower(integration_name)}"

        # Health check configuration
        health_check_endpoint = length(local.normalized_integrations[provider::pyvider::lower(integration_name)].api_endpoints) > 0 ?
          "${local.normalized_integrations[provider::pyvider::lower(integration_name)].api_endpoints[0]}/health" : null

        # Retry configuration
        retry_config = {
          max_retries = 3
          backoff_strategy = "exponential"
          timeout_seconds = 30
        }

        # Logging configuration
        log_prefix = "[${provider::pyvider::lower(integration_name)}]"
        log_level = "info"
      }

      # Generate monitoring labels (must be lowercase for most monitoring systems)
      monitoring_labels = {
        service = provider::pyvider::lower(config.service_name)
        integration = provider::pyvider::lower(integration_name)
        auth_type = local.normalized_integrations[provider::pyvider::lower(integration_name)].auth_type
        environment = "production"
      }
    }
  }

  # Generate integration health checks
  health_checks = {
    for integration_name, config in local.normalized_integrations :
    integration_name => {
      # Health check configuration
      check_name = "health_check_${integration_name}"
      endpoint = config.service_config.health_check_endpoint
      method = "GET"
      timeout = config.service_config.retry_config.timeout_seconds

      # Expected response validation
      expected_status = [200, 204]
      expected_headers = {
        "content-type" = "application/json"
      }

      # Monitoring configuration
      check_interval = "30s"
      failure_threshold = 3
      success_threshold = 1

      # Alert configuration
      alert_on_failure = true
      alert_recipients = ["ops-team@company.com"]
    }
  }

  # Generate Terraform configuration for monitoring
  monitoring_config = {
    for integration_name, config in local.normalized_integrations :
    integration_name => {
      # Prometheus metrics
      metric_name = "service_${integration_name}_health"
      metric_labels = config.monitoring_labels

      # Grafana dashboard configuration
      dashboard_title = "Integration: ${title(integration_name)}"
      dashboard_tags = [integration_name, "integration", "api"]

      # Alert rules
      alert_rules = [
        {
          name = "${integration_name}_service_down"
          expression = "up{service=\"${config.monitoring_labels.service}\"} == 0"
          duration = "5m"
          labels = config.monitoring_labels
          annotations = {
            summary = "Service ${integration_name} is down"
            description = "The ${integration_name} integration service has been down for more than 5 minutes."
          }
        }
      ]
    }
  }
}

output "system_integration" {
  value = {
    normalized_integrations = local.normalized_integrations
    health_checks = local.health_checks
    monitoring = local.monitoring_config
  }
}

## Signature

`lower(input_str: string) -> string`

## Arguments

- **`input_str`** (string, required) - The string to convert to lowercase. Returns `null` if this value is `null`.

## Return Value

Returns a new string with all alphabetic characters converted to lowercase:
- Non-alphabetic characters (numbers, symbols, spaces) remain unchanged
- Returns `null` if the input is `null`
- Returns an empty string if the input is an empty string

## Common Patterns

### Configuration Keys
```terraform
variable "config_key" {
  type = string
}

locals {
  normalized_key = provider::pyvider::lower(var.config_key)
}

resource "pyvider_file_content" "config" {
  filename = "/tmp/app.conf"
  content  = "${local.normalized_key}=value"
}
```

### Filename Generation
```terraform
variable "service_name" {
  type = string
}

locals {
  log_filename = "/var/log/${provider::pyvider::lower(var.service_name)}.log"
}
```

## Related Functions

- [`upper`](./upper.md) - Convert string to uppercase
- [`format`](./format.md) - Format strings with placeholders
- [`replace`](./replace.md) - Replace text patterns in strings