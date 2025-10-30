locals {
  split_split_csv_data = "apple,banana,cherry"
  split_split_split_by_comma = provider::pyvider::split(local.split_split_csv_data, ",")
  # ["apple", "banana", "cherry"]
}

output "split_split_split_by_comma" {
  value = local.split_split_split_by_comma
}
