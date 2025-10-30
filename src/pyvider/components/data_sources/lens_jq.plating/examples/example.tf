data "pyvider_lens_jq" "example" {
  # Configuration options here
}

output "example_data" {
  description = "Data from pyvider_lens_jq"
  value       = data.pyvider_lens_jq.example
}
