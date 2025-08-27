resource "pyvider_file_content" "example" {
  # Configuration options here
}

output "example_id" {
  description = "The ID of the pyvider_file_content resource"
  value       = pyvider_file_content.example.id
}
