---
page_title: "Function: to_snake_case"
description: |-
  Converts text to snake_case format with intelligent word separation
---

# to_snake_case (Function)

> Converts text to snake_case format by replacing spaces and other separators with underscores

The `to_snake_case` function converts text to snake_case format, which uses lowercase letters with underscores separating words. It intelligently handles various input formats including camelCase, PascalCase, kebab-case, and space-separated text.

## When to Use This

- **Variable naming**: Convert user input to valid Python/Terraform variable names
- **File naming**: Create consistent snake_case filenames from titles
- **Database columns**: Standardize column names in snake_case format
- **API endpoints**: Convert display names to API-friendly snake_case paths
- **Configuration keys**: Normalize configuration keys to snake_case

**Anti-patterns (when NOT to use):**
- When preserving original case is important
- For display text that should remain readable
- When working with external APIs that expect specific casing
- For content that contains special formatting

## Quick Start

```terraform
# Convert display text to snake_case
locals {
  page_title = "User Profile Settings"
  snake_name = provider::pyvider::to_snake_case(local.page_title)  # Returns: "user_profile_settings"
}

# Convert camelCase to snake_case
variable "apiEndpointName" {
  default = "getUserData"
}

locals {
  endpoint_snake = provider::pyvider::to_snake_case(var.apiEndpointName)  # Returns: "get_user_data"
}
```

## Examples

### Basic Usage

```terraform
# Standard snake_case conversion
locals {
  various_formats = [
    "User Profile Settings",
    "navigationMenu",
    "data-source-config",
    "API_EndPoint_Handler",
    "Mixed_Format-Text Input"
  ]

  # Convert all to snake_case
  snake_outputs = [
    for text in local.various_formats :
    provider::pyvider::to_snake_case(text)
  ]
  # Results: ["user_profile_settings", "navigation_menu", "data_source_config", "api_end_point_handler", "mixed_format_text_input"]
}

# Different input formats
locals {
  format_examples = {
    camel_case = provider::pyvider::to_snake_case("userProfileData")           # "user_profile_data"
    pascal_case = provider::pyvider::to_snake_case("UserProfileData")         # "user_profile_data"
    kebab_case = provider::pyvider::to_snake_case("user-profile-data")         # "user_profile_data"
    space_separated = provider::pyvider::to_snake_case("user profile data")   # "user_profile_data"
    mixed_separators = provider::pyvider::to_snake_case("User-Profile_Data")  # "user_profile_data"
    already_snake = provider::pyvider::to_snake_case("user_profile_data")     # "user_profile_data"
  }
}

# Edge cases and special handling
locals {
  edge_cases = {
    empty_string = provider::pyvider::to_snake_case("")                    # ""
    single_word = provider::pyvider::to_snake_case("user")                # "user"
    uppercase_word = provider::pyvider::to_snake_case("USER")             # "user"
    with_numbers = provider::pyvider::to_snake_case("user123Profile")     # "user123_profile"
    special_chars = provider::pyvider::to_snake_case("user@profile.com")  # "user_profile_com"
    null_input = provider::pyvider::to_snake_case(null)                   # null
  }
}

output "snake_case_examples" {
  value = {
    conversions = local.snake_outputs
    formats = local.format_examples
    edge_cases = local.edge_cases
  }
}
```

### Database Schema Mapping

```terraform
# Database schema normalization
variable "user_fields" {
  type = list(object({
    display_name = string
    data_type   = string
    is_required = bool
  }))
  default = [
    {
      display_name = "Full Name"
      data_type   = "varchar"
      is_required = true
    },
    {
      display_name = "Email Address"
      data_type   = "varchar"
      is_required = true
    },
    {
      display_name = "Phone Number"
      data_type   = "varchar"
      is_required = false
    },
    {
      display_name = "Date of Birth"
      data_type   = "date"
      is_required = false
    }
  ]
}

# Generate database-friendly column names
locals {
  database_columns = {
    for field in var.user_fields :
    provider::pyvider::to_snake_case(field.display_name) => {
      column_name = provider::pyvider::to_snake_case(field.display_name)
      data_type   = field.data_type
      nullable    = !field.is_required
      original_name = field.display_name
    }
  }
  # Result: {
  #   "full_name" = { column_name = "full_name", data_type = "varchar", nullable = false, original_name = "Full Name" }
  #   "email_address" = { column_name = "email_address", data_type = "varchar", nullable = false, original_name = "Email Address" }
  #   "phone_number" = { column_name = "phone_number", data_type = "varchar", nullable = true, original_name = "Phone Number" }
  #   "date_of_birth" = { column_name = "date_of_birth", data_type = "date", nullable = true, original_name = "Date of Birth" }
  # }

  # Generate CREATE TABLE statement
  create_table_columns = [
    for field in var.user_fields :
    "${provider::pyvider::to_snake_case(field.display_name)} ${field.data_type}${field.is_required ? " NOT NULL" : ""}"
  ]

  create_table_sql = "CREATE TABLE users (\\n  ${join(",\\n  ", local.create_table_columns)}\\n);"
}

# Migration mapping from old to new schema
variable "legacy_columns" {
  type = list(string)
  default = ["userName", "emailAddr", "phoneNum", "birthDate"]
}

locals {
  column_migration = {
    for old_col in var.legacy_columns :
    old_col => {
      old_column = old_col
      new_column = provider::pyvider::to_snake_case(old_col)
      migration_sql = "ALTER TABLE users RENAME COLUMN ${old_col} TO ${provider::pyvider::to_snake_case(old_col)};"
    }
  }
  # Result: {
  #   "userName" = { old_column = "userName", new_column = "user_name", migration_sql = "ALTER TABLE users RENAME COLUMN userName TO user_name;" }
  #   "emailAddr" = { old_column = "emailAddr", new_column = "email_addr", migration_sql = "ALTER TABLE users RENAME COLUMN emailAddr TO email_addr;" }
  #   ...
  # }
}

output "database_mapping" {
  value = {
    columns = local.database_columns
    create_table = local.create_table_sql
    migrations = local.column_migration
  }
}
```

### Python Code Generation

```terraform
# Generate Python variable names from user input
variable "form_fields" {
  type = list(object({
    label = string
    type = string
    required = bool
    validation = string
  }))
  default = [
    {
      label = "First Name"
      type = "text"
      required = true
      validation = "required|string|max:50"
    },
    {
      label = "Company Email"
      type = "email"
      required = true
      validation = "required|email"
    },
    {
      label = "Job Title/Position"
      type = "text"
      required = false
      validation = "string|max:100"
    }
  ]
}

# Generate Python class attributes and validation
locals {
  python_class = {
    for field in var.form_fields :
    provider::pyvider::to_snake_case(field.label) => {
      attribute_name = provider::pyvider::to_snake_case(field.label)
      python_type = field.type == "email" ? "str" : field.type == "text" ? "str" : "str"
      is_optional = !field.required
      validation_rules = field.validation
      original_label = field.label
    }
  }

  # Generate Python class definition
  class_attributes = [
    for field in var.form_fields :
    "    ${provider::pyvider::to_snake_case(field.label)}: ${field.required ? "str" : "Optional[str]"}${field.required ? "" : " = None"}"
  ]

  python_class_definition = join("\\n", [
    "from typing import Optional",
    "from dataclasses import dataclass",
    "",
    "@dataclass",
    "class UserForm:",
    join("\\n", local.class_attributes)
  ])

  # Generate property getters/setters
  python_properties = [
    for field in var.form_fields :
    join("\\n", [
      "    @property",
      "    def ${provider::pyvider::to_snake_case(field.label)}(self) -> ${field.required ? "str" : "Optional[str]"}:",
      "        return self._${provider::pyvider::to_snake_case(field.label)}",
      "",
      "    @${provider::pyvider::to_snake_case(field.label)}.setter",
      "    def ${provider::pyvider::to_snake_case(field.label)}(self, value: ${field.required ? "str" : "Optional[str]"}) -> None:",
      "        self._${provider::pyvider::to_snake_case(field.label)} = value"
    ])
  ]
}

# Configuration file generation
variable "config_sections" {
  type = map(map(string))
  default = {
    "Database Settings" = {
      "Host Name" = "localhost"
      "Port Number" = "5432"
      "Database Name" = "myapp"
    }
    "Cache Configuration" = {
      "Redis Host" = "localhost"
      "Cache TTL Seconds" = "3600"
      "Max Connections" = "10"
    }
  }
}

locals {
  config_snake_case = {
    for section_name, section_config in var.config_sections :
    provider::pyvider::to_snake_case(section_name) => {
      for key, value in section_config :
      provider::pyvider::to_snake_case(key) => value
    }
  }

  # Generate Python config constants
  python_config_constants = flatten([
    for section_name, section_config in var.config_sections : [
      for key, value in section_config :
      "${upper(provider::pyvider::to_snake_case(section_name))}_${upper(provider::pyvider::to_snake_case(key))} = '${value}'"
    ]
  ])

  # Generate environment variable names
  env_var_mapping = flatten([
    for section_name, section_config in var.config_sections : [
      for key, value in section_config : {
        config_key = "${provider::pyvider::to_snake_case(section_name)}.${provider::pyvider::to_snake_case(key)}"
        env_var = "${upper(provider::pyvider::to_snake_case(section_name))}_${upper(provider::pyvider::to_snake_case(key))}"
        original_key = "${section_name}.${key}"
        value = value
      }
    ]
  ])
}

output "python_generation" {
  value = {
    class_definition = local.python_class_definition
    config_constants = local.python_config_constants
    env_variables = local.env_var_mapping
  }
}
```

### File System Operations

```terraform
# File naming from user content
variable "document_titles" {
  type = list(string)
  default = [
    "User Guide & Documentation",
    "API Reference Manual",
    "Installation Instructions (v2.1)",
    "Troubleshooting FAQ",
    "System Architecture Overview"
  ]
}

# Generate filesystem-safe filenames
locals {
  document_files = {
    for title in var.document_titles :
    title => {
      original_title = title
      filename = "${provider::pyvider::to_snake_case(title)}.md"
      directory = "docs/${provider::pyvider::to_snake_case(title)}"
      backup_filename = "${provider::pyvider::to_snake_case(title)}_backup_${formatdate("YYYY_MM_DD", timestamp())}.md"
    }
  }

  # Create directory structure
  doc_directories = [
    for title in var.document_titles :
    "docs/${provider::pyvider::to_snake_case(title)}"
  ]
}

# Log file naming from service names
variable "services" {
  type = list(object({
    name = string
    environment = string
    log_level = string
  }))
  default = [
    {
      name = "User Authentication Service"
      environment = "production"
      log_level = "info"
    },
    {
      name = "Payment Processing API"
      environment = "staging"
      log_level = "debug"
    }
  ]
}

locals {
  service_logging = {
    for service in var.services :
    service.name => {
      service_name = provider::pyvider::to_snake_case(service.name)
      log_filename = "/var/log/${service.environment}/${provider::pyvider::to_snake_case(service.name)}.log"
      error_log = "/var/log/${service.environment}/${provider::pyvider::to_snake_case(service.name)}_error.log"
      access_log = "/var/log/${service.environment}/${provider::pyvider::to_snake_case(service.name)}_access.log"
      config_file = "/etc/${provider::pyvider::to_snake_case(service.name)}/${service.environment}.conf"
      pid_file = "/var/run/${provider::pyvider::to_snake_case(service.name)}.pid"
    }
  }

  # Generate systemd service names
  systemd_services = [
    for service in var.services :
    "${provider::pyvider::to_snake_case(service.name)}_${service.environment}.service"
  ]
}

# Backup and archive naming
variable "backup_sources" {
  type = list(string)
  default = ["User Data Backup", "System Configuration Backup", "Application State Backup"]
}

locals {
  backup_files = {
    for source in var.backup_sources :
    source => {
      daily_backup = "/backups/daily/${provider::pyvider::to_snake_case(source)}_${formatdate("YYYY_MM_DD", timestamp())}.tar.gz"
      weekly_backup = "/backups/weekly/${provider::pyvider::to_snake_case(source)}_week_${formatdate("YYYY_WW", timestamp())}.tar.gz"
      monthly_backup = "/backups/monthly/${provider::pyvider::to_snake_case(source)}_${formatdate("YYYY_MM", timestamp())}.tar.gz"
      latest_symlink = "/backups/${provider::pyvider::to_snake_case(source)}_latest.tar.gz"
    }
  }
}

output "filesystem_operations" {
  value = {
    document_files = local.document_files
    service_logging = local.service_logging
    systemd_services = local.systemd_services
    backup_files = local.backup_files
  }
}
```

## Signature

`to_snake_case(text: string) -> string`

## Arguments

- **`text`** (string, required) - The text to convert to snake_case. Handles various input formats:
  - `camelCase` (userName)
  - `PascalCase` (UserName)
  - `kebab-case` (user-name)
  - `space separated` (user name)
  - `Mixed-Format_text` (mixed separators)
  - If `null`, returns `null`

## Return Value

Returns the converted string in snake_case format:
- **snake_case**: All lowercase with underscores separating words → `user_profile_data`
- **Empty string**: Returns `""` when input is empty
- **Null**: Returns `null` when input is `null`

## Processing Rules

The function applies these transformations:
1. **Convert to lowercase**: All characters converted to lowercase
2. **Replace separators**: Hyphens (`-`), spaces (` `), and existing underscores remain as underscores
3. **Word boundaries**: CamelCase and PascalCase word boundaries become underscores
4. **Clean up**: Multiple consecutive separators become single underscores
5. **Trim**: Leading and trailing separators are removed

## Common Use Cases

```terraform
# Python variable naming
locals {
  variable_name = provider::pyvider::to_snake_case("User Profile Data")  # "user_profile_data"

  # Database column names
  column_name = provider::pyvider::to_snake_case("EmailAddress")  # "email_address"

  # Configuration keys
  config_key = provider::pyvider::to_snake_case("API Secret Key")  # "api_secret_key"

  # File names
  filename = "${provider::pyvider::to_snake_case("System Backup")}.sql"  # "system_backup.sql"
}
```

## Related Functions

- [`to_camel_case`](./to_camel_case.md) - Convert to camelCase format
- [`to_kebab_case`](./to_kebab_case.md) - Convert to kebab-case format
- [`upper`](./upper.md) - Convert to uppercase
- [`lower`](./lower.md) - Convert to lowercase
- [`replace`](./replace.md) - Replace specific text patterns