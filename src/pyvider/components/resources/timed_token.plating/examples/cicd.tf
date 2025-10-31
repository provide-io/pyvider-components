# CI/CD pipeline with temporary tokens

# Generate short-lived token for CI pipeline
resource "pyvider_timed_token" "ci_deploy_token" {
  prefix       = "cicd"
  length       = 32
  duration_sec = 1800  # 30 minutes
  metadata = {
    purpose = "deployment"
    pipeline = "github-actions"
  }
}

# Generate token for automated tests
resource "pyvider_timed_token" "test_runner_token" {
  prefix       = "test"
  length       = 24
  duration_sec = 600  # 10 minutes
  metadata = {
    purpose = "testing"
    environment = "ci"
  }
}

# Create config file with tokens
resource "pyvider_file_content" "ci_config" {
  filename = "/tmp/ci_config.env"
  content = provider::pyvider::join([
    "DEPLOY_TOKEN=${pyvider_timed_token.ci_deploy_token.token}",
    "TEST_TOKEN=${pyvider_timed_token.test_runner_token.token}",
    "EXPIRES_AT=${pyvider_timed_token.ci_deploy_token.expires_at}"
  ], "\n")
}

output "cicd_ci_tokens" {
  value = {
    deploy_token_expires = pyvider_timed_token.ci_deploy_token.expires_at
    test_token_expires = pyvider_timed_token.test_runner_token.expires_at
    config_file = pyvider_file_content.ci_config.filename
  }
  sensitive = true
}
