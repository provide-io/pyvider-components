# Generate a timed token
resource "pyvider_timed_token" "example" {
  prefix       = "demo"
  length       = 32
  duration_sec = 3600  # 1 hour
}

output "basic_token_info" {
  value = {
    token_id   = pyvider_timed_token.example.id
    expires_at = pyvider_timed_token.example.expires_at
  }
  sensitive = true
}
