#!/bin/bash
echo "============================================================"
echo "      🔍 HELL v9.0.4: ULTIMATE PURE ARSENAL"
echo "============================================================"

echo "[*] Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep hell

echo -e "\n[*] Network Deception Listeners:"
for port in 22 80 443 445 88 179 389 502 1433 2222 3306 3389 4455 8080 8443 8888; do
    ss -tuln | grep ":$port " > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "  [✅] Port $port: ACTIVE"
    else
        echo -e "  [❌] Port $port: CLOSED"
    fi
done

echo -e "\n[*] Forensic Pulse (Last 10 lines):"
[ -f logs/hell_activity.log ] && tail -n 10 logs/hell_activity.log || echo "  [!] Log file not found."

echo -e "\n[*] Infrastructure Load:"
uptime | awk '{print "  Load Average: " $10 $11 $12}'
echo "============================================================"
