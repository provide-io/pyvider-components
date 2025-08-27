#!/bin/bash
# Fix all provider.tf files in .garnish-tests

cd /Users/tim/code/gh/provide-io/pyvider-components

for file in .garnish-tests/*/provider.tf; do
    cat > "$file" << 'EOF'
terraform {
  required_providers {
    pyvider = {
      source  = "registry.terraform.io/provide-io/pyvider"
      version = "0.0.3"
    }
  }
}

provider "pyvider" {
  # Provider configuration for tests
}
EOF
    echo "Fixed: $file"
done

echo "All provider.tf files fixed!"
echo "Now run: garnish test"