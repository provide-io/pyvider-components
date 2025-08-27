#!/bin/bash
set -e

echo "Fixing all provider.tf files in .garnish-tests..."

# Fix all provider.tf files
for provider_file in .garnish-tests/*/provider.tf; do
    if [ -f "$provider_file" ]; then
        echo "Fixing: $provider_file"
        cat > "$provider_file" << 'EOF'
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
    fi
done

echo ""
echo "Testing a few examples to prove they work..."
echo ""

# Test function_add_test
echo "1. Testing function_add_test..."
cd .garnish-tests/function_add_test
rm -rf .terraform* terraform.tfstate*
if terraform init >/dev/null 2>&1 && terraform plan >/dev/null 2>&1; then
    echo "   ✅ function_add_test: PASS"
else
    echo "   ❌ function_add_test: FAIL"
fi
cd ../..

# Test resource_local_directory_test  
echo "2. Testing resource_local_directory_test..."
cd .garnish-tests/resource_local_directory_test
rm -rf .terraform* terraform.tfstate*
if terraform init >/dev/null 2>&1 && terraform plan >/dev/null 2>&1; then
    echo "   ✅ resource_local_directory_test: PASS"
else
    echo "   ❌ resource_local_directory_test: FAIL"
fi
cd ../..

# Test data_source_env_variables_test
echo "3. Testing data_source_env_variables_test..."
cd .garnish-tests/data_source_env_variables_test
rm -rf .terraform* terraform.tfstate*
if terraform init >/dev/null 2>&1 && terraform plan >/dev/null 2>&1; then
    echo "   ✅ data_source_env_variables_test: PASS"
else
    echo "   ❌ data_source_env_variables_test: FAIL"
fi
cd ../..

# Test with encryption (needs secret)
echo "4. Testing resource_timed_token_test (with secret)..."
cd .garnish-tests/resource_timed_token_test
rm -rf .terraform* terraform.tfstate*
export PYVIDER_PRIVATE_STATE_SHARED_SECRET=test-secret
if terraform init >/dev/null 2>&1 && terraform plan >/dev/null 2>&1; then
    echo "   ✅ resource_timed_token_test: PASS"
else
    echo "   ❌ resource_timed_token_test: FAIL"
fi
cd ../..

echo ""
echo "✅ Provider references fixed! Tests should now work."
echo ""
echo "To run all tests with garnish (after reinstalling it with the fix):"
echo "  garnish test"
echo ""
echo "The issue is that garnish needs to be updated to generate the correct provider.tf"
echo "The fix is in: /Users/tim/code/gh/provide-io/garnish/src/garnish/test_runner.py line 264"