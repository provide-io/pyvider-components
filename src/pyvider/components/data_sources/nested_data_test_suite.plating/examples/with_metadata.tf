data "pyvider_structured_object_test" "with_metadata" {
  provider   = pyvider.test
  config_name = "production-config"

  metadata = {
    environment = "production"
    region      = "us-west-2"
    owner       = "platform-team"
  }
}

output "settings" {
  description = "Processed settings from metadata"
  value       = data.pyvider_structured_object_test.with_metadata.generated_config.settings
}

output "config_hash" {
  description = "Hash of the configuration name"
  value       = data.pyvider_structured_object_test.with_metadata.summary.config_hash
}
