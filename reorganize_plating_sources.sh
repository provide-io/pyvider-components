#!/bin/bash

# Reorganize source .plating templates so each example .tf file is in its own subdirectory
# This prevents naming conflicts when all examples are loaded by Terraform

SRC_DIR="/REDACTED_ABS_PATH"

# Find all .plating/examples directories
PLATING_DIRS=$(find "$SRC_DIR" -type d -path "*/.plating/examples" 2>/dev/null)

for EXAMPLES_DIR in $PLATING_DIRS; do
    cd "$EXAMPLES_DIR" || continue

    # Get list of .tf files (excluding provider.tf)
    TF_FILES=$(ls *.tf 2>/dev/null | grep -v "^provider.tf$" | grep -v "^example.tf$" || true)

    if [ -z "$TF_FILES" ]; then
        continue
    fi

    # Count non-provider, non-example .tf files
    COUNT=$(echo "$TF_FILES" | wc -w | tr -d ' ')

    if [ "$COUNT" -le 1 ]; then
        # Only one example file, no need to reorganize
        continue
    fi

    echo "Reorganizing source: $EXAMPLES_DIR ($COUNT example files)"

    # For each .tf file, create a subdirectory
    for TF_FILE in $TF_FILES; do
        # Get the base name without extension
        BASENAME=$(basename "$TF_FILE" .tf")

        # Skip if subdirectory already exists
        if [ -d "$BASENAME" ]; then
            echo "  Skipping $BASENAME/ (already exists)"
            continue
        fi

        # Create subdirectory
        mkdir -p "$BASENAME"

        # Move the .tf file to the subdirectory
        mv "$TF_FILE" "$BASENAME/"

        # Copy provider.tf to the subdirectory if it exists
        if [ -f "provider.tf" ]; then
            cp "provider.tf" "$BASENAME/"
        fi

        echo "  Created: $BASENAME/"
    done

    # Delete example.tf if it exists (it's a placeholder)
    if [ -f "example.tf" ]; then
        rm "example.tf"
        echo "  Deleted: example.tf (placeholder)"
    fi

    echo ""
done

echo "Source reorganization complete!"
echo ""
echo "Now regenerate examples with:"
echo "  plating plate --generate-examples --examples-dir examples --component-type function --component-type data_source --component-type resource"
