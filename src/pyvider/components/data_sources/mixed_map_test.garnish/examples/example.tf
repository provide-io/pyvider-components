# Test mixed type maps with various data types
data "pyvider_mixed_map_test" "mixed_config" {
  input_map = {
    string_value = "hello"
    number_value = 42
    bool_value   = true
    list_value   = ["a", "b", "c"]
    nested_map   = {
      inner_key = "inner_value"
      inner_num = 3.14
    }
    null_value   = null
  }
}

output "mixed_map_analysis" {
  value = {
    type_counts = data.pyvider_mixed_map_test.mixed_config.type_counts
    has_nulls   = data.pyvider_mixed_map_test.mixed_config.has_null_values
    depth       = data.pyvider_mixed_map_test.mixed_config.max_depth
  }
}

output "extracted_strings" {
  value = data.pyvider_mixed_map_test.mixed_config.string_values
}

output "extracted_numbers" {
  value = data.pyvider_mixed_map_test.mixed_config.numeric_values
}