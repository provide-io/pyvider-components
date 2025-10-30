#!/usr/bin/env python3
"""
Build documentation and examples, then clean up incorrect duplicates.

This script:
1. Generates documentation using plating
2. Generates executable examples
3. Cleans up incorrect example duplicates caused by shared .plating directories
"""

import asyncio
from pathlib import Path
from plating.plating import Plating
from plating.types import PlatingContext
from provide.foundation import file as foundation_file
from provide.foundation import pout, perr

# Multi-function example names that should be kept everywhere
SHARED_EXAMPLES = {
    "basic",
    "advanced",
    "comprehensive",
    "aggregations",
    "resource_calculations",
}

def cleanup_function_examples(examples_dir: Path):
    """
    Clean up function examples to remove incorrect duplicates.

    For each function in examples/function/{function_name}/:
    - Keep: {function_name}/ subdirectory (the function's own example)
    - Keep: basic/, advanced/, comprehensive/ (shared multi-function examples)
    - Remove: All other function-specific subdirectories
    """
    function_dir = examples_dir / "function"
    if not function_dir.exists():
        return

    removed_count = 0
    kept_count = 0

    # Iterate through each function directory
    for function_path in function_dir.iterdir():
        if not function_path.is_dir():
            continue

        function_name = function_path.name
        pout(f"📦 Cleaning {function_name}...")

        # Check each example subdirectory
        for example_path in function_path.iterdir():
            if not example_path.is_dir():
                continue

            example_name = example_path.name

            # Decide if this example should be kept
            should_keep = (
                example_name == function_name or  # Function's own example
                example_name in SHARED_EXAMPLES    # Shared multi-function example
            )

            if should_keep:
                kept_count += 1
            else:
                # Remove this incorrect duplicate
                pout(f"  ❌ Removing {function_name}/{example_name}/")
                foundation_file.safe_rmtree(example_path, missing_ok=True)
                removed_count += 1

    pout(f"\n✅ Cleanup complete: kept {kept_count}, removed {removed_count} duplicate examples")

async def build_docs_and_examples(overwrite: bool = False):
    """Build documentation and clean examples."""

    # Check if examples already exist
    examples_dir = Path("examples")
    if examples_dir.exists() and not overwrite:
        perr("⚠️  Examples directory already exists. Use --overwrite to regenerate.")
        return

    # Generate documentation
    pout("🍽️  Generating documentation...")
    context = PlatingContext(provider_name="pyvider")
    api = Plating(context, "pyvider.components")
    result = await api.plate()

    pout(f"✅ Generated {result.files_generated} documentation files")

    # Generate examples (use CLI for this since it has the flag)
    pout("\n📁 Generating executable examples...")
    import subprocess
    cmd = ["plating", "plate", "--provider-name", "pyvider",
           "--package-name", "pyvider.components", "--generate-examples"]
    subprocess.run(cmd, check=True)

    # Clean up function examples
    pout("\n🧹 Cleaning up duplicate examples...")
    cleanup_function_examples(examples_dir)

    pout("\n✨ Build complete!")

if __name__ == "__main__":
    import sys
    overwrite = "--overwrite" in sys.argv
    asyncio.run(build_docs_and_examples(overwrite=overwrite))
