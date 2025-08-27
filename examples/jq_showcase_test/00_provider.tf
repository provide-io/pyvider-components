terraform {
  required_providers {
    pyvider = {
      source  = "local/providers/pyvider"
      version = "0.0.3"
    }
  }
}

provider "pyvider" {
  api_token = "placeholder-token"
}
