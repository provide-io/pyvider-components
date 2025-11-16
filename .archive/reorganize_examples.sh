#!/bin/bash

# Reorganize examples so each .tf file (except provider.tf) is in its own subdirectory
# This allows each example to be tested independently without conflicts

BASE_DIR="/REDACTED_ABS_PATH"

# Find all example directories
EXAMPLE_DIRS=$(find "$BASE_DIR" -type d -mindepth 2 -maxdepth 2 | sort)

for DIR in $EXAMPLE_DIRS; do
    cd "$DIR" || continue

    # Check if there are multiple .tf files (excluding provider.tf)
    TF_FILES=$(ls *.tf 2>/dev/null | grep -v "^provider.tf$" || true)

    if [ -z "$TF_FILES" ]; then
        continue
    fi

    # Count non-provider .tf files
    COUNT=$(echo "$TF_FILES" | wc -w | tr -d ' ')

    if [ "$COUNT" -le 1 ]; then
        # Only one example file, no need to reorganize
        continue
    fi

    echo "Reorganizing: $DIR ($COUNT example files)"

    # For each .tf file (except provider.tf), create a subdirectory
    for TF_FILE in $TF_FILES; do
        if [ "$TF_FILE" != "provider.tf" ]; then
            # Get the base name without extension
            BASENAME=$(basename "$TF_FILE" .tf)

            # Create subdirectory
            mkdir -p "$BASENAME"

            # Move the .tf file to the subdirectory
            mv "$TF_FILE" "$BASENAME/"

            # Copy provider.tf to the subdirectory
            if [ -f "provider.tf" ]; then
                cp "provider.tf" "$BASENAME/"
            fi

            echo "  Created: $BASENAME/"
        fi
    done

    echo ""
done

echo "Reorganization complete!"
