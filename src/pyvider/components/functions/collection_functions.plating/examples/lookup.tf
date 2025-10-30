locals {
  settings = {
    database_host = "db.example.com"
    database_port = 5432
  }
  db_host = provider::pyvider::lookup(local.settings, "database_host", "localhost")
  missing = provider::pyvider::lookup(local.settings, "missing_key", "default")
}

output "lookup_example" {
  value = {
    found    = local.db_host
    notfound = local.missing
  }
}
