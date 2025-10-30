#!/usr/bin/env python3
"""
Build documentation and examples.

This script:
1. Generates documentation using plating
2. Generates executable examples
"""

import asyncio
from pathlib import Path
from plating.plating import Plating
from plating.types import PlatingContext
from provide.foundation import pout, perr

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

    pout("\n✨ Build complete!")

if __name__ == "__main__":
    import sys
    overwrite = "--overwrite" in sys.argv
    asyncio.run(build_docs_and_examples(overwrite=overwrite))
