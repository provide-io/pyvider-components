#!/bin/dash
# Simple system benchmark - pure POSIX shell

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                  SYSTEM BENCHMARK                        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Running quick system performance tests..."
echo ""

# CPU test - calculate pi digits
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CPU Test (Integer Math)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
START=$(date +%s%N 2>/dev/null || date +%s)
i=0
while [ $i -lt 100000 ]; do
    result=$((i * i))
    i=$((i + 1))
done
END=$(date +%s%N 2>/dev/null || date +%s)
if echo "$START" | grep -q "N"; then
    # Nanosecond precision unavailable
    DURATION=$((END - START))
    echo "  Duration: ${DURATION}s"
else
    DURATION=$(((END - START) / 1000000))
    echo "  Duration: ${DURATION}ms"
fi
echo "  Operations: 100,000 integer multiplications"
echo ""

# Disk I/O test
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Disk I/O Test (Sequential Write)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
TMPFILE="/tmp/dash-bench-$$"
START=$(date +%s)
dd if=/dev/zero of="$TMPFILE" bs=1M count=10 2>&1 | grep -v records
END=$(date +%s)
DURATION=$((END - START))
rm -f "$TMPFILE"
if [ $DURATION -gt 0 ]; then
    SPEED=$((10 / DURATION))
    echo "  Speed: ~${SPEED} MB/s"
else
    echo "  Speed: >10 MB/s (very fast!)"
fi
echo "  Size: 10 MB"
echo ""

# Memory allocation test
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Memory Test (String Operations)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
START=$(date +%s)
i=0
str=""
while [ $i -lt 1000 ]; do
    str="${str}x"
    i=$((i + 1))
done
END=$(date +%s)
DURATION=$((END - START))
echo "  Duration: ${DURATION}s"
echo "  Operations: 1,000 string concatenations"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Benchmark Complete"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Note: These are simple tests for demonstration purposes."
echo "For serious benchmarking, use tools like sysbench or stress-ng."
echo ""
