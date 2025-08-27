terraform {
  required_providers {
    pyvider = {
      source  = "local/providers/pyvider"
      version = "0.0.3"
    }
  }
}

# The provider requires the encryption key to be set.
provider "pyvider" {}
