data "pyvider_http_api" "example" {
  url = "https://httpbin.org/get"
}

output "example_data" {
  description = "Data from pyvider_http_api"
  value       = data.pyvider_http_api.example
}
