#!/usr/bin/env python3
"""
Package helper for node-sysmon.

This Python script is ONLY used during PACKAGING, not execution!
It helps prepare the Node.js binary and JavaScript code for PSPF packaging.

At runtime, only Node.js executes - no Python!
"""

import os
import subprocess
import sys
from pathlib import Path


def check_node_binary():
    """Check if we have a Node.js binary to package."""
    bin_dir = Path(__file__).parent / "bin"
    node_path = bin_dir / "node"

    if node_path.exists():
        print(f"✅ Found Node.js binary: {node_path}")

        # Check version
        try:
            result = subprocess.run(
                [str(node_path), "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            print(f"   Version: {result.stdout.strip()}")
        except Exception as e:
            print(f"   ⚠️  Could not check version: {e}")

        # Check file type
        result = subprocess.run(
            ["file", str(node_path)],
            capture_output=True,
            text=True
        )
        print(f"   Type: {result.stdout.strip()}")

        # Check size
        size_mb = node_path.stat().st_size / (1024 * 1024)
        print(f"   Size: {size_mb:.1f} MB")

        # Check if static or dynamic
        result = subprocess.run(
            ["ldd", str(node_path)],
            capture_output=True,
            text=True
        )
        if "statically linked" in result.stdout or "not a dynamic" in result.stderr:
            print("   ✅ Statically linked - no runtime dependencies!")
        else:
            print("   ⚠️  Dynamically linked - requires libc on target")
            deps = result.stdout.strip().split('\n')
            print(f"   Dependencies: {len(deps)} libraries")

        return True
    else:
        print(f"❌ Node.js binary not found at: {node_path}")
        print("")
        print("To package node-sysmon, you need a Node.js binary.")
        print("")
        print("Option 1: Use system Node.js")
        print("  mkdir -p bin")
        print("  cp $(which node) bin/node")
        print("")
        print("Option 2: Download specific version")
        print("  # From nodejs.org official binaries")
        print("  wget https://nodejs.org/dist/v22.11.0/node-v22.11.0-linux-x64.tar.xz")
        print("  tar xf node-v22.11.0-linux-x64.tar.xz")
        print("  cp node-v22.11.0-linux-x64/bin/node bin/")
        print("")
        return False


def check_javascript():
    """Check if JavaScript code is present."""
    js_file = Path(__file__).parent / "sysmon.js"
    pkg_file = Path(__file__).parent / "package.json"

    all_found = True

    if js_file.exists():
        lines = len(js_file.read_text().split('\n'))
        print(f"✅ Found: sysmon.js ({lines} lines)")
    else:
        print(f"❌ Missing: sysmon.js")
        all_found = False

    if pkg_file.exists():
        print(f"✅ Found: package.json")
    else:
        print(f"❌ Missing: package.json")
        all_found = False

    return all_found


def main():
    """Entry point for package helper."""
    print("=" * 60)
    print("Node.js System Monitor - Package Helper")
    print("=" * 60)
    print("")
    print("This script prepares node-sysmon for packaging.")
    print("Python is ONLY used during build, not at runtime!")
    print("")

    # Check components
    has_binary = check_node_binary()
    print("")
    has_js = check_javascript()
    print("")

    if has_binary and has_js:
        print("✅ All components ready for packaging!")
        print("")
        print("To build the package:")
        print("  flavor pack --manifest pyproject.toml --output node-sysmon.psp")
        print("")
        print("Alternative (using JSON manifest with Go/Rust builder):")
        print("  flavor-rs-builder --manifest manifest.json --output node-sysmon.psp")
        print("")
        print("To run the package:")
        print("  ./node-sysmon.psp sysinfo")
        print("  ./node-sysmon.psp network")
        print("  ./node-sysmon.psp --json")
        print("")
        print("The package will contain:")
        print("  - Node.js binary (~118 MB → ~40 MB gzip)")
        print("  - JavaScript code (~10 KB)")
        print("  - Total size: ~40-45 MB")
        print("")
        print("NO Python runtime in the final package!")
        sys.exit(0)
    else:
        print("❌ Missing required components")
        print("   Please prepare Node.js binary before packaging.")
        sys.exit(1)


if __name__ == "__main__":
    main()
