locals {
  csv_data = "apple,banana,cherry"
  split_by_comma = provider::pyvider::split(local.csv_data, ",")
  # ["apple", "banana", "cherry"]
}

output "split_example" {
  value = local.split_by_comma
}
