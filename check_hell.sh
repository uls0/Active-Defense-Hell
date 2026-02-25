#!/bin/bash
echo "============================================================"
echo "      🔍 HELL v10.5.0: FULL ARSENAL CHECK"
echo "============================================================"

echo "[*] Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep hell

echo -e "\n[*] Network Deception Listeners:"
# Lista completa de puertos v10.5.0
for port in 22 80 443 445 88 179 389 502 1433 2222 3306 3389 4455 8080 8443 8888; do
    ss -tuln | grep ":$port " > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "  [✅] Port $port: ACTIVE"
    else
        echo -e "  [❌] Port $port: CLOSED"
    fi
done

echo -e "\n[*] Forensic Pulse (Last 3 events):"
[ -f logs/hell_activity.log ] && tail -n 3 logs/hell_activity.log || echo "  [!] No log activity detected yet."

echo -e "\n[*] Infrastructure Load:"
uptime | awk '{print "  Load Average: " $10 $11 $12}'
echo "============================================================"
