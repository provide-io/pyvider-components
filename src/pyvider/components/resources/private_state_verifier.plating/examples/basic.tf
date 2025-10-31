# Verify encryption of private state
resource "pyvider_private_state_verifier" "test" {
  input_value = "sensitive-data"
}

output "basic_verification" {
  value = {
    verified      = pyvider_private_state_verifier.test.verification_successful
    hash_length   = pyvider_private_state_verifier.test.output_hash_length
    is_encrypted  = pyvider_private_state_verifier.test.state_is_encrypted
  }
}
