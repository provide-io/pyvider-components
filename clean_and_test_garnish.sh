#!/bin/bash
# Clean all lock files and test with local provider

echo "Cleaning all .terraform.lock.hcl files in .garnish-tests..."
find .garnish-tests -name ".terraform.lock.hcl" -delete
find .garnish-tests -name ".terraform" -type d -exec rm -rf {} + 2>/dev/null || true

echo "Testing with local provider at: ~/.terraform.d/plugins/local/providers/pyvider/0.1.0/"

cd .garnish-tests/function_add_test
echo "Testing function_add_test..."
terraform init
terraform plan

echo ""
echo "If this works, run: garnish test"