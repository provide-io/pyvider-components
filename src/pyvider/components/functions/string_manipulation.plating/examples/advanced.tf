# Advanced string manipulation and chaining

# Email normalization
locals {
  user_emails = [
    "  JOHN.DOE@EXAMPLE.COM  ",
    "jane.smith@Example.COM",
    "BOB_JONES@example.com"
  ]

  normalized_emails = [
    for email in local.user_emails :
    provider::pyvider::lower(
      provider::pyvider::replace(
        provider::pyvider::replace(email, " ", ""),
        "_", "."
      )
    )
  ]
}

# Slug generation for URLs
locals {
  article_titles = [
    "How to Use Terraform Providers",
    "Advanced Pyvider Patterns!",
    "String Manipulation 101"
  ]

  article_slugs = [
    for title in local.article_titles :
    provider::pyvider::to_kebab_case(
      provider::pyvider::replace(
        provider::pyvider::lower(title),
        "[^a-z0-9\\s-]",
        ""
      )
    )
  ]
}

# Template building with multiple formats
locals {
  user_data = {
    first_name = "john"
    last_name = "doe"
    role = "engineer"
  }

  # Build formatted strings
  display_name = provider::pyvider::format("{} {}", [
    provider::pyvider::to_camel_case(local.user_data.first_name, true),
    provider::pyvider::to_camel_case(local.user_data.last_name, true)
  ])

  username = provider::pyvider::join([
    provider::pyvider::lower(local.user_data.first_name),
    provider::pyvider::lower(local.user_data.last_name)
  ], ".")

  role_display = provider::pyvider::upper(local.user_data.role)
}

# CSV parsing and transformation
locals {
  csv_line = "name,email,department,active"
  parsed_headers = provider::pyvider::split(local.csv_line, ",")

  # Transform to object keys
  object_keys = [
    for header in local.parsed_headers :
    provider::pyvider::to_snake_case(header)
  ]
}

# Complex text processing
locals {
  raw_text = "Product Name: Widget-2000  Price: $99.99  Stock: 50 units"

  # Extract and normalize
  parts = provider::pyvider::split(local.raw_text, "  ")
  product_name = provider::pyvider::replace(
    provider::pyvider::split(local.parts[0], ": ")[1],
    "-",
    "_"
  )
}

output "advanced_string_results" {
  value = {
    normalized_emails = local.normalized_emails
    article_slugs = local.article_slugs
    user_profile = {
      display_name = local.display_name
      username = local.username
      role = local.role_display
    }
    csv_processing = {
      headers = local.parsed_headers
      transformed_keys = local.object_keys
    }
  }
}
