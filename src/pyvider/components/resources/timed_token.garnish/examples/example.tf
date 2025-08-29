resource "pyvider_timed_token" "example" {
  # Configuration options here
}

output "example_id" {
  description = "The ID of the pyvider_timed_token resource"
  value       = pyvider_timed_token.example.id
}
