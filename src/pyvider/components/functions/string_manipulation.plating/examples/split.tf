locals {
  split_csv_data = "apple,banana,cherry"
  split_split_by_comma = provider::pyvider::split(local.split_csv_data, ",")
  # ["apple", "banana", "cherry"]
}

output "split_example" {
  value = local.split_split_by_comma
}
