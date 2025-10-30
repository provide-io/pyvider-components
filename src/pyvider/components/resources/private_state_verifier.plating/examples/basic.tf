provider "pyvider" {
  alias     = "test"
  test_mode = true
}

# Verify encryption of private state
resource "pyvider_private_state_verifier" "test" {
  provider   = pyvider.test
  input_value = "sensitive-data"
}

output "verification" {
  value = {
    input_value       = pyvider_private_state_verifier.test.input_value
    decrypted_token   = pyvider_private_state_verifier.test.decrypted_token
    expected_token    = "SECRET_FOR_${upper(pyvider_private_state_verifier.test.input_value)}"
    matches_expected  = pyvider_private_state_verifier.test.decrypted_token == "SECRET_FOR_${upper(pyvider_private_state_verifier.test.input_value)}"
  }
}
