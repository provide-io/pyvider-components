# Advanced string manipulation and chaining

# Email normalization
locals {
  adv_user_emails = [
    "  JOHN.DOE@EXAMPLE.COM  ",
    "jane.smith@Example.COM",
    "BOB_JONES@example.com"
  ]

  adv_normalized_emails = [
    for email in local.adv_user_emails :
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
  adv_article_titles = [
    "How to Use Terraform Providers",
    "Advanced Pyvider Patterns!",
    "String Manipulation 101"
  ]

  adv_article_slugs = [
    for title in local.adv_article_titles :
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
  adv_user_data = {
    first_name = "john"
    last_name = "doe"
    role = "engineer"
  }

  # Build formatted strings
  adv_display_name = provider::pyvider::format("{} {}", [
    provider::pyvider::to_camel_case(local.adv_user_data.first_name, true),
    provider::pyvider::to_camel_case(local.adv_user_data.last_name, true)
  ])

  adv_username = provider::pyvider::join([
    provider::pyvider::lower(local.adv_user_data.first_name),
    provider::pyvider::lower(local.adv_user_data.last_name)
  ], ".")

  adv_role_display = provider::pyvider::upper(local.adv_user_data.role)
}

# CSV parsing and transformation
locals {
  adv_csv_line = "name,email,department,active"
  adv_parsed_headers = provider::pyvider::split(local.adv_csv_line, ",")

  # Transform to object keys
  adv_object_keys = [
    for header in local.adv_parsed_headers :
    provider::pyvider::to_snake_case(header)
  ]
}

# Complex text processing
locals {
  adv_raw_text = "Product Name: Widget-2000  Price: $99.99  Stock: 50 units"

  # Extract and normalize
  adv_parts = provider::pyvider::split(local.adv_raw_text, "  ")
  adv_product_name = provider::pyvider::replace(
    provider::pyvider::split(local.adv_parts[0], ": ")[1],
    "-",
    "_"
  )
}

output "advanced_string_results" {
  value = {
    normalized_emails = local.adv_normalized_emails
    article_slugs = local.adv_article_slugs
    user_profile = {
      display_name = local.adv_display_name
      username = local.adv_username
      role = local.adv_role_display
    }
    csv_processing = {
      headers = local.adv_parsed_headers
      transformed_keys = local.adv_object_keys
    }
  }
}
