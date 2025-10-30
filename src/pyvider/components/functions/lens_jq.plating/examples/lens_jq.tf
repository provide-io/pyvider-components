locals {
  lens_jq_user_data = {
    id    = 123
    name  = "Alice Johnson"
    email = "alice@example.com"
  }

  lens_jq_user_name  = provider::pyvider::lens_jq(local.lens_jq_user_data, ".name")    # "Alice Johnson"
  lens_jq_user_email = provider::pyvider::lens_jq(local.lens_jq_user_data, ".email")   # "alice@example.com"
}

output "lens_jq_example" {
  value = {
    name  = local.lens_jq_user_name
    email = local.lens_jq_user_email
  }
}
