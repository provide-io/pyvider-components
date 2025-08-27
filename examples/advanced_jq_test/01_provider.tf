terraform {
  #backend "local" { path = ".soup/tfdata/terraform.tfstate" }
  required_providers { pyvider = { source = "registry.terraform.io/provide-io/pyvider", version = "0.0.3" } }
}
provider "pyvider" { api_token = "placeholder-token" }
