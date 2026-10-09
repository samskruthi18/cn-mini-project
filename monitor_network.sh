
#!/bin/bash
set -e

mkdir -p reports
REPORT="reports/network_$(date +%Y%m%d_%H%M%S).txt"

{
    echo
    echo "===== BANDWIDTH LIMIT STATISTICS ====="
    sudo tc -s qdisc show dev s1-eth3
} | tee "$REPORT"

echo
echo "Report saved to: $REPORT"
