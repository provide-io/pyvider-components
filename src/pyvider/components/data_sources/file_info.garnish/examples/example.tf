data "pyvider_file_info" "example" {
  # Configuration options here
}

output "example_data" {
  description = "Data from pyvider_file_info"
  value       = data.pyvider_file_info.example
}
