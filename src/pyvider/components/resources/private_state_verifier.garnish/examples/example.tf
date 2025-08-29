resource "pyvider_private_state_verifier" "example" {
  # Configuration options here
}

output "example_id" {
  description = "The ID of the pyvider_private_state_verifier resource"
  value       = pyvider_private_state_verifier.example.id
}
