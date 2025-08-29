resource "pyvider_local_directory" "example" {
  # Configuration options here
}

output "example_id" {
  description = "The ID of the pyvider_local_directory resource"
  value       = pyvider_local_directory.example.id
}
