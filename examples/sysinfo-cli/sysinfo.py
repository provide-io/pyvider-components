#!/usr/bin/env python3
"""System Information CLI Tool - A demonstration of FlavorPack packaging.

This tool provides detailed system information in a beautiful format,
packaged as a single executable using PSPF/2025 format.
"""

import argparse
import os
import platform
import sys
from datetime import datetime
from pathlib import Path


def get_system_info():
    """Gather comprehensive system information."""
    return {
        "System": platform.system(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor() or "Unknown",
        "Architecture": " ".join(platform.architecture()),
        "Hostname": platform.node(),
        "Python Version": platform.python_version(),
        "Python Implementation": platform.python_implementation(),
        "Python Compiler": platform.python_compiler(),
    }


def get_environment_info():
    """Gather environment information."""
    home = os.environ.get("HOME", "Unknown")
    user = os.environ.get("USER", "Unknown")
    shell = os.environ.get("SHELL", "Unknown")
    path_count = len(os.environ.get("PATH", "").split(":"))
    
    return {
        "User": user,
        "Home": home,
        "Shell": shell,
        "PATH Entries": path_count,
        "Environment Variables": len(os.environ),
    }


def get_process_info():
    """Gather process information."""
    return {
        "Process ID": os.getpid(),
        "Parent PID": os.getppid(),
        "Executable": sys.executable,
        "Working Directory": os.getcwd(),
    }


def format_section(title, data, width=60):
    """Format a section with a title and data."""
    lines = []
    lines.append("=" * width)
    lines.append(f"  {title}")
    lines.append("=" * width)
    
    max_key_len = max(len(k) for k in data.keys())
    
    for key, value in data.items():
        lines.append(f"  {key:<{max_key_len}} : {value}")
    
    lines.append("")
    return "\n".join(lines)


def main():
    """Main entry point for sysinfo CLI."""
    parser = argparse.ArgumentParser(
        description="System Information Tool (packaged with FlavorPack)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sysinfo              Show all system information
  sysinfo --system     Show only system details
  sysinfo --env        Show only environment details
  sysinfo --process    Show only process details
  
This tool is packaged using FlavorPack (PSPF/2025 format).
No installation required - just run the executable!
        """
    )
    
    parser.add_argument("--system", action="store_true",
                       help="Show only system information")
    parser.add_argument("--env", action="store_true",
                       help="Show only environment information")
    parser.add_argument("--process", action="store_true",
                       help="Show only process information")
    parser.add_argument("--json", action="store_true",
                       help="Output in JSON format")
    parser.add_argument("--version", action="version",
                       version="sysinfo 1.0.0 (FlavorPack packaged)")
    
    args = parser.parse_args()
    
    # Determine what to show
    show_all = not (args.system or args.env or args.process)
    
    # Gather information
    data = {}
    if show_all or args.system:
        data["System Information"] = get_system_info()
    if show_all or args.env:
        data["Environment"] = get_environment_info()
    if show_all or args.process:
        data["Process Information"] = get_process_info()
    
    # Output
    if args.json:
        import json
        print(json.dumps(data, indent=2))
    else:
        print()
        print("╔" + "═" * 58 + "╗")
        print("║" + " SYSTEM INFORMATION TOOL ".center(58) + "║")
        print("║" + f" Packaged with FlavorPack (PSPF/2025) ".center(58) + "║")
        print("║" + f" Timestamp: {datetime.now().isoformat()} ".center(58) + "║")
        print("╚" + "═" * 58 + "╝")
        print()
        
        for section_title, section_data in data.items():
            print(format_section(section_title, section_data))
        
        print("=" * 60)
        print("  FlavorPack: https://github.com/provide-io/flavorpack")
        print("=" * 60)


if __name__ == "__main__":
    main()
