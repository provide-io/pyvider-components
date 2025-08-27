#!/bin/bash
# Test each example individually

EXAMPLES_DIR="/Users/tim/code/gh/provide-io/pyvider-components/examples"
FAILING_TESTS=(
    "encryption_test"
    "integrated_test"
    "jq_showcase_test"
    "local_directory_test"
    "private_state_test"
    "provider_config_test"
    "stdlib_functions_test"
)

for test in "${FAILING_TESTS[@]}"; do
    echo "========================================="
    echo "Testing: $test"
    echo "========================================="
    cd "$EXAMPLES_DIR/$test" || continue
    
    # Clean previous state
    rm -rf .terraform* terraform.tfstate* .soup 2>/dev/null
    
    # Initialize
    echo "Initializing..."
    if ! terraform init -upgrade >/dev/null 2>&1; then
        echo "❌ Init failed for $test"
        continue
    fi
    
    # Validate
    echo "Validating..."
    if ! terraform validate >/dev/null 2>&1; then
        echo "❌ Validation failed for $test"
        terraform validate 2>&1 | head -20
        continue
    fi
    
    # Plan
    echo "Planning..."
    if terraform plan -out=tfplan >/dev/null 2>&1; then
        echo "✅ $test works!"
    else
        echo "❌ Plan failed for $test"
        terraform plan 2>&1 | grep -A5 "Error:" | head -20
    fi
    
    echo ""
done