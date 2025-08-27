# Basic file content resource example
resource "pyvider_file_content" "config" {
  filename = "${path.module}/config.json"
  content = jsonencode({
    name    = "example-app"
    version = "1.0.0"
    created = timestamp()
  })
}

output "file_path" {
  description = "Path to the created file"
  value       = pyvider_file_content.config.filename
}

output "file_hash" {
  description = "SHA256 hash of the file content"
  value       = pyvider_file_content.config.content_hash
}