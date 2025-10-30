# Basic type conversion function examples

# Example 1: Number to string conversions
locals {
  comp_integer = 42
  comp_float   = 3.14159

  comp_int_string   = provider::pyvider::tostring(local.comp_integer) # "42"
  comp_float_string = provider::pyvider::tostring(local.comp_float)   # "3.14159"
}

# Example 2: Boolean to string conversions
locals {
  comp_is_enabled = true
  comp_is_debug   = false

  comp_enabled_str = provider::pyvider::tostring(local.comp_is_enabled) # "true"
  comp_debug_str   = provider::pyvider::tostring(local.comp_is_debug)   # "false"
}

# Example 3: List to string conversions
locals {
  comp_numbers = [1, 2, 3, 4, 5]
  comp_colors  = ["red", "green", "blue"]

  comp_numbers_str = provider::pyvider::tostring(local.comp_numbers) # "[1, 2, 3, 4, 5]"
  comp_colors_str  = provider::pyvider::tostring(local.comp_colors)  # '["red", "green", "blue"]'
}

# Example 4: Map to string conversions
locals {
  comp_config = {
    comp_host = "localhost"
    comp_port = 8080
    comp_ssl  = true
  }

  config_str = provider::pyvider::tostring(local.comp_config) # '{"host": "localhost", "port": 8080, "ssl": true}'
}

# Example 5: Practical use in string interpolation
locals {
  comp_server_port = 8080
  comp_use_ssl     = true

  comp_connection_info = "Server running on port ${provider::pyvider::tostring(local.comp_server_port)} (SSL: ${provider::pyvider::tostring(local.comp_use_ssl)})"
}

# Create output file
resource "pyvider_file_content" "conversion_examples" {
  filename = "/tmp/type_conversion_examples.txt"
  content = join("\n", [
    "Type Conversion Examples",
    "========================",
    "",
    "Integer: ${local.comp_int_string}",
    "Float: ${local.comp_float_string}",
    "Boolean: ${local.comp_enabled_str}",
    "List: ${local.comp_numbers_str}",
    "Map: ${local.config_str}",
    "",
    "Connection: ${local.comp_connection_info}"
  ])
}

output "conversion_results" {
  value = {
    integer_str = local.comp_int_string
    float_str   = local.comp_float_string
    boolean_str = local.comp_enabled_str
    list_str    = local.comp_numbers_str
    map_str     = local.config_str
    example     = local.comp_connection_info
  }
}
