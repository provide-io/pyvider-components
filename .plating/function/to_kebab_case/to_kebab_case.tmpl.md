---
page_title: "Function: to_kebab_case"
description: |-
  Converts text to kebab-case format with lowercase letters and hyphens
---

# to_kebab_case (Function)

> Converts text to kebab-case format by replacing separators with hyphens and using lowercase

The `to_kebab_case` function converts text to kebab-case format, which uses lowercase letters with hyphens separating words. This format is commonly used in URLs, CSS classes, and HTML attributes.

## When to Use This

- **URL slugs**: Create SEO-friendly URLs from page titles
- **CSS class names**: Generate consistent CSS class naming
- **HTML attributes**: Create valid HTML data attributes
- **File names**: Generate web-safe filenames
- **Configuration keys**: Use in systems that prefer kebab-case

**Anti-patterns (when NOT to use):**
- JavaScript variable names (use camelCase instead)
- Database column names (use snake_case instead)
- When preserving original case is important
- For content that needs to remain readable

## Quick Start

```terraform
# Convert page title to URL slug
locals {
  page_title = "User Profile Settings"
  url_slug = provider::pyvider::to_kebab_case(local.page_title)  # Returns: "user-profile-settings"
}

# Convert to CSS class name
variable "component_name" {
  default = "navigationMenu"
}

locals {
  css_class = provider::pyvider::to_kebab_case(var.component_name)  # Returns: "navigation-menu"
}
```

## Examples

### Basic Usage

{{ example("basic") }}

### URL Generation

{{ example("url_generation") }}

### CSS Integration

{{ example("css_integration") }}

## Schema

{{ schema() }}

## Common Patterns

### URL Slug Generation
```terraform
variable "blog_posts" {
  type = list(object({
    title = string
    content = string
  }))
  default = [
    {
      title = "Getting Started with Terraform"
      content = "Introduction to infrastructure as code..."
    },
    {
      title = "Advanced Provider Development"
      content = "Building custom Terraform providers..."
    }
  ]
}

locals {
  # Generate URL-friendly slugs
  post_urls = {
    for post in var.blog_posts :
    provider::pyvider::to_kebab_case(post.title) => {
      title = post.title
      url = "/blog/${provider::pyvider::to_kebab_case(post.title)}"
    }
  }
}
```

### CSS Class Generation
```terraform
variable "ui_components" {
  type = list(string)
  default = [
    "primaryButton",
    "navigationMenu",
    "userProfileCard",
    "searchInputField"
  ]
}

locals {
  # Generate CSS classes
  css_classes = [
    for component in var.ui_components :
    provider::pyvider::to_kebab_case(component)
  ]
}

resource "pyvider_file_content" "css_styles" {
  filename = "/tmp/components.css"
  content = join("\n", [
    for class_name in local.css_classes :
    ".${class_name} {\n  /* Component styles */\n}"
  ])
}
```

### HTML Data Attributes
```terraform
variable "data_attributes" {
  type = map(string)
  default = {
    "userId" = "12345"
    "profileType" = "premium"
    "lastLoginTime" = "2024-01-15T10:30:00Z"
  }
}

locals {
  # Convert to kebab-case data attributes
  html_attributes = {
    for key, value in var.data_attributes :
    "data-${provider::pyvider::to_kebab_case(key)}" => value
  }
}
```

### Configuration File Generation
```terraform
variable "app_settings" {
  type = map(any)
  default = {
    "apiBaseUrl" = "https://api.example.com"
    "cacheTimeout" = 300
    "debugMode" = false
  }
}

resource "pyvider_file_content" "yaml_config" {
  filename = "/tmp/config.yaml"
  content = join("\n", [
    for key, value in var.app_settings :
    "${provider::pyvider::to_kebab_case(key)}: ${jsonencode(value)}"
  ])
}
```

## Input Format Handling

The function handles various input formats:

| Input Format | Example | Output |
|--------------|---------|--------|
| camelCase | "userName" | "user-name" |
| PascalCase | "UserProfile" | "user-profile" |
| snake_case | "user_name" | "user-name" |
| Space-separated | "User Name" | "user-name" |
| UPPER_CASE | "USER_NAME" | "user-name" |
| Mixed | "userProfile_ID" | "user-profile-id" |

## Error Handling

### Null Input
```terraform
locals {
  # Returns null for null input
  null_result = provider::pyvider::to_kebab_case(null)  # Returns: null
}
```

### Empty String
```terraform
locals {
  # Returns empty string for empty input
  empty_result = provider::pyvider::to_kebab_case("")  # Returns: ""
}
```

### Special Characters
```terraform
locals {
  # Handles special characters gracefully
  special_chars = provider::pyvider::to_kebab_case("user@name#123")  # Returns: "user-name-123"
}
```

## Best Practices

### 1. URL-Safe Characters Only
```terraform
variable "page_title" {
  type = string
  validation {
    condition     = length(var.page_title) > 0 && length(var.page_title) <= 100
    error_message = "Page title must be between 1 and 100 characters."
  }
}

locals {
  safe_slug = provider::pyvider::to_kebab_case(var.page_title)
}
```

### 2. Combine with Length Validation
```terraform
locals {
  input_text = "Very Long Component Name That Might Be Too Long"
  kebab_result = provider::pyvider::to_kebab_case(local.input_text)

  # Truncate if too long
  final_result = provider::pyvider::length(local.kebab_result) > 50 ?
    "${substr(local.kebab_result, 0, 47)}..." :
    local.kebab_result
}
```

### 3. Web-Safe File Names
```terraform
variable "document_titles" {
  type = list(string)
  default = [
    "User Manual v2.1",
    "API Documentation",
    "Installation Guide"
  ]
}

locals {
  # Generate web-safe file names
  file_names = [
    for title in var.document_titles :
    "${provider::pyvider::to_kebab_case(title)}.html"
  ]
}
```

## Web Development Integration

### Generate HTML Components
```terraform
variable "page_sections" {
  type = list(object({
    name = string
    content = string
  }))
  default = [
    { name = "heroSection", content = "Welcome to our site" },
    { name = "featuresOverview", content = "Key features" }
  ]
}

resource "pyvider_file_content" "html_template" {
  filename = "/tmp/page.html"
  content = join("\n", [
    for section in var.page_sections :
    "<div class=\"${provider::pyvider::to_kebab_case(section.name)}\">\n  ${section.content}\n</div>"
  ])
}
```

### API Route Generation
```terraform
variable "api_endpoints" {
  type = list(string)
  default = [
    "getUserProfile",
    "updateUserSettings",
    "deleteUserAccount"
  ]
}

locals {
  # Generate REST API routes
  api_routes = [
    for endpoint in var.api_endpoints :
    "/api/${provider::pyvider::to_kebab_case(endpoint)}"
  ]
}
```

## SEO Considerations

- **URL Structure**: Kebab-case URLs are preferred by search engines
- **Readability**: Hyphens are treated as word separators in URLs
- **Length**: Keep slugs concise but descriptive
- **Keywords**: Preserve important keywords in the conversion

## Performance Considerations

- **Fast conversion**: Efficient string processing with minimal overhead
- **Memory efficient**: No significant memory allocation
- **Caching friendly**: Deterministic results suitable for caching
- **Batch processing**: Optimized for processing multiple strings

## Related Functions

- [`to_snake_case`](./to_snake_case.md) - Convert to snake_case format
- [`to_camel_case`](./to_camel_case.md) - Convert to camelCase format
- [`lower`](./lower.md) - Convert to lowercase
- [`replace`](./replace.md) - Replace specific text patterns
- [`split`](./split.md) - Split strings for processing