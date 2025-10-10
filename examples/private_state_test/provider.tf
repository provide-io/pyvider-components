terraform {
  required_providers {
    pyvider = {
      source  = "local/providers/pyvider"
      version = "0.0.6"
    }
  }
}

# The provider requires the encryption key to be set.
provider "pyvider" {}
