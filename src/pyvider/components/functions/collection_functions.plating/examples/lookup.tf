locals {
  lookup_settings = {
    lookup_database_host = "db.example.com"
    lookup_database_port = 5432
  }
  db_host = provider::pyvider::lookup(local.lookup_settings, "database_host", "localhost")
  missing = provider::pyvider::lookup(local.lookup_settings, "missing_key", "default")
}

output "lookup_database_host" {
  value = {
    found    = local.db_host
    notfound = local.missing
  }
}
