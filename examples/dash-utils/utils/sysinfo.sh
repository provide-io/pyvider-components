#!/bin/dash
# System information utility - pure POSIX shell

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                  SYSTEM INFORMATION                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Operating System
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Operating System"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo "  Distribution: $NAME"
    echo "  Version:      $VERSION"
else
    echo "  Kernel:       $(uname -s)"
    echo "  Release:      $(uname -r)"
fi
echo "  Architecture: $(uname -m)"
echo "  Hostname:     $(hostname)"
echo ""

# CPU Information
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CPU"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f /proc/cpuinfo ]; then
    CPU_MODEL=$(grep "model name" /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)
    CPU_CORES=$(grep -c "^processor" /proc/cpuinfo)
    echo "  Model:  $CPU_MODEL"
    echo "  Cores:  $CPU_CORES"
else
    echo "  Cores:  $(sysctl -n hw.ncpu 2>/dev/null || echo 'Unknown')"
fi
echo ""

# Memory Information
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Memory"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f /proc/meminfo ]; then
    MEM_TOTAL=$(grep "MemTotal:" /proc/meminfo | awk '{print int($2/1024)" MB"}')
    MEM_FREE=$(grep "MemAvailable:" /proc/meminfo | awk '{print int($2/1024)" MB"}')
    echo "  Total:     $MEM_TOTAL"
    echo "  Available: $MEM_FREE"
else
    echo "  Total:     $(sysctl -n hw.memsize 2>/dev/null | awk '{print int($1/1024/1024)" MB"}' || echo 'Unknown')"
fi
echo ""

# Uptime
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "System Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Uptime:    $(uptime | sed 's/.*up//' | sed 's/,.*user.*//' | xargs)"
echo "  Load Avg:  $(uptime | awk -F'load average:' '{print $2}' | xargs)"
echo ""

# Disk Space
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Disk Space (Root)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
df -h / | tail -1 | awk '{printf "  Total: %s\n  Used:  %s (%s)\n  Avail: %s\n", $2, $3, $5, $4}'
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Shell: dash (Debian Almquist Shell)"
echo "Script: Pure POSIX sh - no Python required!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
