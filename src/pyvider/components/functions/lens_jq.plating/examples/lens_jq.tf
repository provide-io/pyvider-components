locals {
  lens_jq_lens_jq_user_data = {
    lens_jq_lens_jq_id    = 123
    lens_jq_lens_jq_name  = "Alice Johnson"
    lens_jq_lens_jq_email = "alice@example.com"
  }

  user_name  = provider::pyvider::lens_jq(local.lens_jq_lens_jq_user_data, ".name")    # "Alice Johnson"
  user_email = provider::pyvider::lens_jq(local.lens_jq_lens_jq_user_data, ".email")   # "alice@example.com"
}

output "lens_jq_lens_jq_user_data" {
  value = {
    name  = local.user_name
    email = local.user_email
  }
}
