#!/usr/bin/env python3
"""
Package helper for dash-utils.

This Python script is ONLY used during PACKAGING, not execution!
It helps prepare the dash binary and scripts for inclusion in the PSPF package.

At runtime, only dash and shell scripts are executed - no Python!
"""

import os
import subprocess
import sys
from pathlib import Path


def check_dash_binary():
    """Check if we have a dash binary to package."""
    bin_dir = Path(__file__).parent / "bin"
    dash_path = bin_dir / "dash"

    if dash_path.exists():
        print(f"✅ Found dash binary: {dash_path}")
        # Check if it's static
        result = subprocess.run(
            ["file", str(dash_path)],
            capture_output=True,
            text=True
        )
        print(f"   Type: {result.stdout.strip()}")

        result = subprocess.run(
            ["ldd", str(dash_path)],
            capture_output=True,
            text=True
        )
        if "statically linked" in result.stdout or "not a dynamic" in result.stderr:
            print("   ✅ Statically linked - no runtime dependencies!")
        else:
            print("   ⚠️  Dynamically linked - may require libc on target")
            print(f"   Dependencies:\n{result.stdout}")

        return True
    else:
        print(f"❌ Dash binary not found at: {dash_path}")
        print("")
        print("To package dash-utils, you need a static dash binary.")
        print("")
        print("Option 1: Use system dash (if musl-based)")
        print("  mkdir -p bin")
        print("  cp /bin/dash bin/dash")
        print("")
        print("Option 2: Use busybox dash (statically linked)")
        print("  mkdir -p bin")
        print("  busybox --install -s bin/")
        print("")
        print("Option 3: Download pre-built static dash")
        print("  # From Alpine Linux (musl-based)")
        print("  docker run --rm alpine cat /bin/dash > bin/dash")
        print("  chmod +x bin/dash")
        print("")
        return False


def check_scripts():
    """Check if all scripts are present."""
    scripts_dir = Path(__file__).parent / "scripts"

    if not scripts_dir.exists():
        # Create scripts symlink to current directory for packaging
        os.symlink(".", scripts_dir)
        print("✅ Created scripts directory link")

    required_scripts = [
        "dash-utils.sh",
        "utils/sysinfo.sh",
        "utils/diskusage.sh",
        "utils/procmon.sh",
        "utils/netinfo.sh",
        "utils/benchmark.sh",
    ]

    all_found = True
    for script in required_scripts:
        script_path = Path(__file__).parent / script
        if script_path.exists():
            print(f"✅ Found: {script}")
        else:
            print(f"❌ Missing: {script}")
            all_found = False

    return all_found


def main():
    """Entry point for package helper."""
    print("=" * 60)
    print("Dash Utils Package Helper")
    print("=" * 60)
    print("")
    print("This script prepares dash-utils for packaging.")
    print("Python is ONLY used during build, not at runtime!")
    print("")

    # Check components
    has_binary = check_dash_binary()
    print("")
    has_scripts = check_scripts()
    print("")

    if has_binary and has_scripts:
        print("✅ All components ready for packaging!")
        print("")
        print("To build the package:")
        print("  flavor pack --manifest pyproject.toml --output dash-utils.psp")
        print("")
        print("To run the package:")
        print("  ./dash-utils.psp sysinfo")
        print("  ./dash-utils.psp procmon")
        print("")
        print("The package will contain:")
        print("  - Static dash binary (~100-200 KB)")
        print("  - Shell scripts (~10 KB)")
        print("  - Total size: ~300-500 KB (tiny!)")
        print("")
        print("NO Python runtime in the final package!")
        sys.exit(0)
    else:
        print("❌ Missing required components")
        print("   Please prepare the dash binary before packaging.")
        sys.exit(1)


if __name__ == "__main__":
    main()
