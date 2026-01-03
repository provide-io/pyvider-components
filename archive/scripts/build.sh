#!/bin/bash
# Build documentation and examples
#
# Usage:
#   ./scripts/build.sh           # Build if examples don't exist
#   ./scripts/build.sh --overwrite # Force rebuild

set -e

cd "$(dirname "$0")/.."

python3 scripts/build_docs_and_examples.py "$@"
