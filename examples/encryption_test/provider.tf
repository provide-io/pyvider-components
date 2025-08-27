terraform {
  required_providers {
    pyvider = {
      source  = "local/providers/pyvider"
      version = "0.0.3"
    }
  }
}

# The provider block is empty. The framework will require the
# PYVIDER_PRIVATE_STATE_KEY environment variable to be set.
provider "pyvider" {}
