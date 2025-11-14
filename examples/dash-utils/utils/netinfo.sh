#!/bin/dash
# Network information utility - pure POSIX shell

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                 NETWORK INFORMATION                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Network interfaces
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Network Interfaces"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v ip >/dev/null 2>&1; then
    ip -brief addr show | while read iface state addr rest; do
        echo "  $iface: $state - $addr"
    done
elif command -v ifconfig >/dev/null 2>&1; then
    ifconfig | grep "^[a-z]" | awk '{print "  " $1 " " $2}'
else
    echo "  No network tools available"
fi
echo ""

# Routing
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Default Gateway"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v ip >/dev/null 2>&1; then
    ip route show default | head -1 | awk '{print "  Gateway: " $3 " via " $5}'
elif command -v netstat >/dev/null 2>&1; then
    netstat -rn | grep "^0.0.0.0" | awk '{print "  Gateway: " $2}'
fi
echo ""

# DNS
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DNS Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f /etc/resolv.conf ]; then
    grep "^nameserver" /etc/resolv.conf | head -3 | awk '{print "  Nameserver: " $2}'
else
    echo "  No DNS configuration found"
fi
echo ""

# Listening ports
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Listening Ports (Top 10)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if command -v ss >/dev/null 2>&1; then
    ss -tlnp 2>/dev/null | grep LISTEN | head -10 | \
        awk '{print "  " $4}' | sed 's/.*:/Port: /'
elif command -v netstat >/dev/null 2>&1; then
    netstat -tlnp 2>/dev/null | grep LISTEN | head -10 | \
        awk '{print "  Port: " $4}' | sed 's/.*://'
fi
echo ""
