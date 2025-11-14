#!/bin/dash
# Process monitor - pure POSIX shell

TOP_N="${1:-20}"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                   PROCESS MONITOR                        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Process count
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Process Statistics"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
TOTAL_PROCS=$(ps aux | wc -l)
echo "  Total Processes: $((TOTAL_PROCS - 1))"
echo ""

# Top processes by CPU
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Top $TOP_N Processes by CPU Usage"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "  %-7s  %-5s  %-5s  %s\n" "PID" "%CPU" "%MEM" "COMMAND"
echo "  ────────────────────────────────────────────────────────"
ps aux --sort=-%cpu 2>/dev/null | head -$((TOP_N + 1)) | tail -$TOP_N | \
    awk '{printf "  %-7s  %-5s  %-5s  %s\n", $2, $3"%", $4"%", $11}' || \
ps aux | sort -rn -k 3 | head -$TOP_N | \
    awk '{printf "  %-7s  %-5s  %-5s  %s\n", $2, $3"%", $4"%", $11}'
echo ""

# Top processes by Memory
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Top $TOP_N Processes by Memory Usage"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "  %-7s  %-5s  %-5s  %s\n" "PID" "%CPU" "%MEM" "COMMAND"
echo "  ────────────────────────────────────────────────────────"
ps aux --sort=-%mem 2>/dev/null | head -$((TOP_N + 1)) | tail -$TOP_N | \
    awk '{printf "  %-7s  %-5s  %-5s  %s\n", $2, $3"%", $4"%", $11}' || \
ps aux | sort -rn -k 4 | head -$TOP_N | \
    awk '{printf "  %-7s  %-5s  %-5s  %s\n", $2, $3"%", $4"%", $11}'
echo ""
