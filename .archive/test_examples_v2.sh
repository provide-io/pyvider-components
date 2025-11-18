#!/bin/bash

# Test all generated examples (including subdirectories)
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL=0
PASSED=0
FAILED=0
FAILED_DIRS=()

# Base directory
BASE_DIR="/Users/tim/code/gh/provide-io/pyvider-components/examples"

# Find all directories that contain .tf files (at any depth level)
EXAMPLE_DIRS=$(find "$BASE_DIR" -type f -name "*.tf" -exec dirname {} \; | sort -u)

echo "========================================="
echo "Testing Pyvider Component Examples"
echo "========================================="
echo ""

for DIR in $EXAMPLE_DIRS; do
    # Skip directories that only contain provider.tf
    NON_PROVIDER_COUNT=$(ls "$DIR"/*.tf 2>/dev/null | grep -v "/provider.tf$" | wc -l | tr -d ' ')

    if [ "$NON_PROVIDER_COUNT" -eq 0 ]; then
        continue
    fi

    TOTAL=$((TOTAL + 1))
    REL_PATH=$(echo "$DIR" | sed "s|$BASE_DIR/||")

    echo -e "${YELLOW}Testing: $REL_PATH${NC}"

    cd "$DIR" || continue

    # Clean up any existing terraform state
    rm -rf .terraform .terraform.lock.hcl terraform.tfstate terraform.tfstate.backup 2>/dev/null

    # Test init
    echo "  Running tofu init..."
    if ! tofu init >/dev/null 2>&1; then
        echo -e "${RED}  ✗ FAILED: tofu init${NC}"
        FAILED=$((FAILED + 1))
        FAILED_DIRS+=("$REL_PATH (init)")
        echo ""
        continue
    fi

    # Test plan
    echo "  Running tofu plan..."
    if ! tofu plan >/dev/null 2>&1; then
        echo -e "${RED}  ✗ FAILED: tofu plan${NC}"
        FAILED=$((FAILED + 1))
        FAILED_DIRS+=("$REL_PATH (plan)")
        echo ""
        continue
    fi

    # Test apply
    echo "  Running tofu apply..."
    if ! tofu apply -auto-approve >/dev/null 2>&1; then
        echo -e "${RED}  ✗ FAILED: tofu apply${NC}"
        FAILED=$((FAILED + 1))
        FAILED_DIRS+=("$REL_PATH (apply)")
        echo ""
        continue
    fi

    # Clean up
    tofu destroy -auto-approve >/dev/null 2>&1
    rm -rf .terraform .terraform.lock.hcl terraform.tfstate terraform.tfstate.backup 2>/dev/null

    echo -e "${GREEN}  ✓ PASSED${NC}"
    PASSED=$((PASSED + 1))
    echo ""
done

# Summary
echo "========================================="
echo "Test Summary"
echo "========================================="
echo "Total: $TOTAL"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"

if [ $FAILED -gt 0 ]; then
    echo ""
    echo "Failed examples:"
    for FAILED_DIR in "${FAILED_DIRS[@]}"; do
        echo -e "  ${RED}✗ $FAILED_DIR${NC}"
    done
    exit 1
fi

echo ""
echo -e "${GREEN}All tests passed!${NC}"
exit 0
