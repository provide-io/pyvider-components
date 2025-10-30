# Config file generation with templates

locals {
  app_config = {
    name = "my-application"
    version = "1.0.0"
    port = 8080
    database = {
      host = "localhost"
      port = 5432
      name = "myapp"
    }
    features = ["api", "web", "admin"]
  }

  # Build nginx config
  nginx_config = provider::pyvider::join([
    "server {",
    "  listen ${local.app_config.port};",
    "  server_name ${local.app_config.name};",
    "",
    "  location / {",
    "    proxy_pass http://localhost:3000;",
    "  }",
    "}"
  ], "\n")

  # Build env file
  env_file = provider::pyvider::join([
    "APP_NAME=${local.app_config.name}",
    "APP_VERSION=${local.app_config.version}",
    "APP_PORT=${local.app_config.port}",
    "DB_HOST=${local.app_config.database.host}",
    "DB_PORT=${local.app_config.database.port}",
    "DB_NAME=${local.app_config.database.name}"
  ], "\n")
}

resource "pyvider_file_content" "nginx_config" {
  filename = "/tmp/${local.app_config.name}-nginx.conf"
  content  = local.nginx_config
}

resource "pyvider_file_content" "env_file" {
  filename = "/tmp/${local.app_config.name}.env"
  content  = local.env_file
}

output "generated_files" {
  value = {
    nginx = pyvider_file_content.nginx_config.filename
    env   = pyvider_file_content.env_file.filename
  }
}
