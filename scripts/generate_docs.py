#!/usr/bin/env python3
"""Generate documentation for Pyvider components using the Plating API."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Literal

# Add plating to path
sys.path.append("../plating/src")

from plating.api import PlatingAPI
from plating.types import ComponentType


def generate_documentation(
    component_type: Literal["function", "resource", "data_source", "all"],
    output_dir: str,
) -> None:
    """Generate documentation for specified component types.

    Args:
        component_type: Type of components to generate docs for
        output_dir: Base directory for documentation output
    """
    api = PlatingAPI()
    output_path = Path(output_dir)

    if component_type == "function":
        output_path = output_path / "functions"
        output_path.mkdir(parents=True, exist_ok=True)
        result = asyncio.run(
            api._plating.plate(output_path, component_types=[ComponentType.FUNCTION])
        )
        files = [(fp, fp.read_text(encoding="utf-8")) for fp in result.output_files]
        written = api.write_generated_files(files)
        print(f"✅ Generated {len(written)} function documentation files")

    elif component_type == "resource":
        output_path = output_path / "resources"
        output_path.mkdir(parents=True, exist_ok=True)
        result = asyncio.run(
            api._plating.plate(output_path, component_types=[ComponentType.RESOURCE])
        )
        files = [(fp, fp.read_text(encoding="utf-8")) for fp in result.output_files]
        written = api.write_generated_files(files)
        print(f"✅ Generated {len(written)} resource documentation files")

    elif component_type == "data_source":
        output_path = output_path / "data_sources"
        output_path.mkdir(parents=True, exist_ok=True)
        result = asyncio.run(
            api._plating.plate(output_path, component_types=[ComponentType.DATA_SOURCE])
        )
        files = [(fp, fp.read_text(encoding="utf-8")) for fp in result.output_files]
        written = api.write_generated_files(files)
        print(f"✅ Generated {len(written)} data source documentation files")

    elif component_type == "all":
        # Generate all types
        for comp_type in ["function", "resource", "data_source"]:
            generate_documentation(comp_type, output_dir)  # type: ignore
    else:
        print(f"❌ Unknown component type: {component_type}")
        sys.exit(1)


def main() -> None:
    """Main entry point for documentation generation."""
    if len(sys.argv) != 3:
        print("Usage: generate_docs.py <component_type> <output_dir>")
        print("  component_type: function | resource | data_source | all")
        print("  output_dir: Base directory for documentation output")
        sys.exit(1)

    component_type = sys.argv[1]
    output_dir = sys.argv[2]

    if component_type not in ["function", "resource", "data_source", "all"]:
        print(f"❌ Invalid component type: {component_type}")
        print("Valid types: function, resource, data_source, all")
        sys.exit(1)

    print(f"📚 Generating {component_type} documentation...")
    generate_documentation(component_type, output_dir)  # type: ignore


if __name__ == "__main__":
    main()
