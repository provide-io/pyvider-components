#!/bin/bash
# Update all provider.tf files to use registry

cd /Users/tim/code/gh/provide-io/pyvider-components/.garnish-tests

for dir in */; do
    echo "Updating ${dir}provider.tf"
    cat > "${dir}provider.tf" << 'EOF'
terraform {
  required_providers {
    pyvider = {
      source  = "registry.terraform.io/provide-io/pyvider"
      version = "0.0.3"
    }
  }
}

provider "pyvider" {}
EOF
done

echo "All provider.tf files updated!"