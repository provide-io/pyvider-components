data "pyvider_simple_map_test" "empty" {
  provider = pyvider.test
  # No input_data provided - will use empty map
}

output "empty_result" {
  description = "Result when no input data is provided"
  value       = data.pyvider_simple_map_test.empty.processed_data
}
