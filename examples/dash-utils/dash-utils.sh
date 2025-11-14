#!/bin/dash
# Main entry point for dash-utils toolkit
# This demonstrates packaging shell scripts with FlavorPack

VERSION="1.0.0"

show_help() {
    cat << 'EOF'
╔══════════════════════════════════════════════════════════╗
║              DASH UTILITIES TOOLKIT                      ║
║         Packaged with FlavorPack (PSPF/2025)             ║
╚══════════════════════════════════════════════════════════╝

Usage: dash-utils <command> [options]

Commands:
  sysinfo     Show system information
  diskusage   Show disk usage statistics
  netinfo     Show network information
  procmon     Monitor processes
  benchmark   Run system benchmark
  help        Show this help message
  version     Show version

Examples:
  dash-utils sysinfo
  dash-utils diskusage /home
  dash-utils procmon --top 10

This is a pure shell script package - no Python required!
All scripts are written in POSIX sh and use only standard UNIX tools.

Packaged using FlavorPack PSPF/2025 format.
EOF
}

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
UTILS_DIR="$SCRIPT_DIR/utils"

# Parse command
case "${1:-help}" in
    sysinfo)
        shift
        exec "$UTILS_DIR/sysinfo.sh" "$@"
        ;;
    diskusage)
        shift
        exec "$UTILS_DIR/diskusage.sh" "$@"
        ;;
    netinfo)
        shift
        exec "$UTILS_DIR/netinfo.sh" "$@"
        ;;
    procmon)
        shift
        exec "$UTILS_DIR/procmon.sh" "$@"
        ;;
    benchmark)
        shift
        exec "$UTILS_DIR/benchmark.sh" "$@"
        ;;
    version)
        echo "dash-utils version $VERSION"
        echo "Packaged with FlavorPack PSPF/2025"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Error: Unknown command '$1'" >&2
        echo "Run 'dash-utils help' for usage information" >&2
        exit 1
        ;;
esac
