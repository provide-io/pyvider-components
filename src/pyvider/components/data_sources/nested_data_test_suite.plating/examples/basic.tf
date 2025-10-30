provider "pyvider" {
  alias     = "test"
  test_mode = true
}

data "pyvider_structured_object_test" "basic" {
  provider   = pyvider.test
  config_name = "my-config"
}

output "generated_config" {
  description = "Generated configuration object with nested attributes"
  value       = data.pyvider_structured_object_test.basic.generated_config
}

output "summary" {
  description = "Summary information with nested details"
  value       = data.pyvider_structured_object_test.basic.summary
}
