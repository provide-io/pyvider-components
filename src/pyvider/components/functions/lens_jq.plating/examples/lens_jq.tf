locals {
  user_data = {
    id    = 123
    name  = "Alice Johnson"
    email = "alice@example.com"
  }

  user_name  = provider::pyvider::lens_jq(local.user_data, ".name")    # "Alice Johnson"
  user_email = provider::pyvider::lens_jq(local.user_data, ".email")   # "alice@example.com"
}

output "lens_jq_example" {
  value = {
    name  = local.user_name
    email = local.user_email
  }
}
