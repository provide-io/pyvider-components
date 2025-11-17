data "pyvider_http_api" "example" {
  # Configuration options here
}

output "example_data" {
  description = "Data from pyvider_http_api"
  value       = data.pyvider_http_api.example
}
