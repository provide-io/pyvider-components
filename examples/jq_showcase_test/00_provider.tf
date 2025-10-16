terraform {
  required_providers {
    pyvider = {
      #source  = "local/providers/pyvider"
      source = "registry.terraform.io/provide-io/pyvider"
      version = "0.0.10"
    }
  }
}

provider "pyvider" {
  api_token = "placeholder-token"
}


