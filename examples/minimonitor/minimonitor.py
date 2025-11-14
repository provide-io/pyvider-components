#!/usr/bin/env python3
"""
Mini System Monitor - Proof of Concept
Demonstrates the same packaging pattern as Glances, using only stdlib.
"""

import argparse
import json
import os
import platform
import sys
import time
from datetime import datetime


def get_cpu_info():
    """Get CPU information."""
    try:
        with open('/proc/stat', 'r') as f:
            cpu_line = f.readline()
            cpu_values = cpu_line.split()[1:]
            total_time = sum(int(x) for x in cpu_values)
            idle_time = int(cpu_values[3])
            return {
                "cores": os.cpu_count() or 1,
                "total_time": total_time,
                "idle_time": idle_time,
            }
    except:
        return {"cores": os.cpu_count() or 1, "total_time": 0, "idle_time": 0}


def get_memory_info():
    """Get memory information."""
    try:
        meminfo = {}
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().split()[0]
                    meminfo[key] = int(value) * 1024  # Convert KB to bytes

        total = meminfo.get('MemTotal', 0)
        available = meminfo.get('MemAvailable', 0)
        used = total - available
        percent = (used / total * 100) if total > 0 else 0

        return {
            "total": total,
            "used": used,
            "available": available,
            "percent": round(percent, 1)
        }
    except:
        return {"total": 0, "used": 0, "available": 0, "percent": 0}


def get_disk_info():
    """Get disk information."""
    try:
        stat = os.statvfs('/')
        total = stat.f_blocks * stat.f_frsize
        free = stat.f_bavail * stat.f_frsize
        used = total - free
        percent = (used / total * 100) if total > 0 else 0

        return {
            "total": total,
            "used": used,
            "free": free,
            "percent": round(percent, 1)
        }
    except:
        return {"total": 0, "used": 0, "free": 0, "percent": 0}


def format_bytes(bytes_val):
    """Format bytes to human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} PB"


def display_tui(data):
    """Display monitoring data in TUI format (like glances/htop)."""
    print("\033[2J\033[H")  # Clear screen
    print("╔══════════════════════════════════════════════════════════╗")
    print("║           MINI SYSTEM MONITOR (Glances-like)            ║")
    print("║           Packaged with FlavorPack (PSPF/2025)           ║")
    print(f"║          {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # CPU
    cpu = data['cpu']
    print(f"🖥️  CPU")
    print(f"   Cores: {cpu['cores']}")
    if cpu['total_time'] > 0:
        idle_pct = (cpu['idle_time'] / cpu['total_time']) * 100
        used_pct = 100 - idle_pct
        print(f"   Usage: {used_pct:.1f}% (estimated)")
    print()

    # Memory
    mem = data['memory']
    print(f"💾 Memory")
    print(f"   Total:     {format_bytes(mem['total'])}")
    print(f"   Used:      {format_bytes(mem['used'])} ({mem['percent']}%)")
    print(f"   Available: {format_bytes(mem['available'])}")

    # Progress bar
    bar_width = 40
    filled = int(bar_width * mem['percent'] / 100)
    bar = '█' * filled + '░' * (bar_width - filled)
    print(f"   [{bar}]")
    print()

    # Disk
    disk = data['disk']
    print(f"💿 Disk (/)")
    print(f"   Total: {format_bytes(disk['total'])}")
    print(f"   Used:  {format_bytes(disk['used'])} ({disk['percent']}%)")
    print(f"   Free:  {format_bytes(disk['free'])}")

    # Progress bar
    filled = int(bar_width * disk['percent'] / 100)
    bar = '█' * filled + '░' * (bar_width - filled)
    print(f"   [{bar}]")
    print()

    # System info
    print(f"📊 System")
    print(f"   OS:       {platform.system()} {platform.release()}")
    print(f"   Hostname: {platform.node()}")
    print(f"   Python:   {platform.python_version()}")
    print()
    print("Press Ctrl+C to exit")


def monitor_loop(interval=2, json_output=False):
    """Main monitoring loop."""
    try:
        while True:
            data = {
                "timestamp": datetime.now().isoformat(),
                "cpu": get_cpu_info(),
                "memory": get_memory_info(),
                "disk": get_disk_info(),
            }

            if json_output:
                print(json.dumps(data, indent=2))
                time.sleep(interval)
            else:
                display_tui(data)
                time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped")
        sys.exit(0)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Mini System Monitor (Glances-like demo)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  minimonitor              Monitor system (TUI mode)
  minimonitor --json       Output JSON for automation
  minimonitor -t 5         Refresh every 5 seconds

This demonstrates the same packaging pattern as Glances:
- Real-time system monitoring
- Terminal UI mode
- JSON output mode
- Packagable with FlavorPack

The real Glances has 30+ dependencies, but the packaging
pattern is identical!
"""
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output JSON instead of TUI'
    )

    parser.add_argument(
        '-t', '--time',
        type=int,
        default=2,
        metavar='SECONDS',
        help='Refresh interval in seconds (default: 2)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0 (Glances-like demo)'
    )

    args = parser.parse_args()

    print(f"🚀 Starting Mini System Monitor...")
    print(f"   Refresh: every {args.time} seconds")
    print(f"   Mode: {'JSON' if args.json else 'TUI'}")
    print()
    time.sleep(1)

    monitor_loop(interval=args.time, json_output=args.json)


if __name__ == "__main__":
    main()
