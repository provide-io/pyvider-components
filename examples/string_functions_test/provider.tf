#
# provider.tf
#

terraform {
  required_providers {
    pyvider = {
      source = "local/providers/pyvider"
      version = "0.0.6"
    }
  }
}

provider "pyvider" {
  api_token = "Asdf1asdfasdfasdf"
}
