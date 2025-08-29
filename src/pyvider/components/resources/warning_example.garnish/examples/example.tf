resource "pyvider_warning_example" "example" {
  # Configuration options here
}

output "example_id" {
  description = "The ID of the pyvider_warning_example resource"
  value       = pyvider_warning_example.example.id
}
