locals {
  lookup_lookup_settings = {
    lookup_lookup_database_host = "db.example.com"
    lookup_lookup_database_port = 5432
  }
  db_host = provider::pyvider::lookup(local.lookup_lookup_settings, "database_host", "localhost")
  missing = provider::pyvider::lookup(local.lookup_lookup_settings, "missing_key", "default")
}

output "lookup_lookup_settings" {
  value = {
    found    = local.db_host
    notfound = local.missing
  }
}
