#!/bin/dash
# Disk usage analyzer - pure POSIX shell

TARGET="${1:-.}"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                   DISK USAGE ANALYZER                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Analyzing: $TARGET"
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
du -sh "$TARGET" 2>/dev/null | awk '{print "  Total Size: " $1}'
echo ""

# Top directories
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Largest Directories (Top 10)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
du -h "$TARGET" 2>/dev/null | sort -rh | head -11 | tail -10 | \
    awk '{printf "  %-10s  %s\n", $1, $2}'
echo ""

# File type breakdown
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "File Count by Type"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d "$TARGET" ]; then
    TOTAL_FILES=$(find "$TARGET" -type f 2>/dev/null | wc -l)
    TOTAL_DIRS=$(find "$TARGET" -type d 2>/dev/null | wc -l)
    echo "  Files:       $TOTAL_FILES"
    echo "  Directories: $TOTAL_DIRS"
fi
echo ""
