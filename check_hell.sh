#!/bin/bash
echo "============================================================"
echo "      🔍 HELL INFRASTRUCTURE PRE-FLIGHT CHECK"
echo "============================================================"

echo "[*] Checking Docker Containers..."
docker ps --format "table {{.Names}}\t{{.Status}}" | grep hell

echo -e "\n[*] Checking Network Listeners (Host Mode)..."
for port in 80 445 3306 8888 2222 4455; do
    ss -tuln | grep ":$port " > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "  [✅] Port $port is OPEN and LISTENING."
    else
        echo -e "  [❌] Port $port is CLOSED."
    fi
done

echo -e "\n[*] Checking Log Activity (Last 3 lines)..."
[ -f logs/hell_activity.log ] && tail -n 3 logs/hell_activity.log || echo "  [!] Log file not found yet."

echo -e "\n[*] Memory Status..."
free -h | grep Mem
echo "============================================================"
