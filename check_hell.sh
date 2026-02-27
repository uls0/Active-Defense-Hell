#!/bin/bash
echo "============================================================"
echo "      🔍 HELL v9.0.4: ULTIMATE PURE ARSENAL"
echo "============================================================"

echo "[*] Container Status:"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep hell

echo -e "\n[*] Network Deception Listeners:"
# Puertos base
for port in 22 80 443 445 88 179 389 502 1433 2222 3306 3389 4455 8080 8443 8888 33001 1338 8545 3333 18080; do
    ss -tuln | grep ":$port " > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "  [✅] Port $port: ACTIVE"
    else
        echo -e "  [❌] Port $port: CLOSED"
    fi
done

# Resumen del rango Tarpit
ACTIVE_TARPIT=$(ss -tuln | grep -E ":20[0-9]{3}" | wc -l)
if [ $ACTIVE_TARPIT -gt 0 ]; then
    echo -e "  [✅] Port Range 20000-20100: ACTIVE ($ACTIVE_TARPIT ports)"
else
    echo -e "  [❌] Port Range 20000-20100: CLOSED"
fi

echo -e "\n[*] Forensic Pulse (Last 10 lines):"
[ -f logs/hell_activity.log ] && tail -n 10 logs/hell_activity.log || echo "  [!] Log file not found."

echo -e "\n[*] Lethal Engagement Monitor (Top Connections):"
ss -tnp | grep python3 | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr | head -n 10 || echo "  [!] No active engagements."

echo -e "\n[*] Resource Culprit (Top Threads):"
ps -eo pid,ppid,pcpu,pmem,comm,args --sort=-pcpu | grep python | head -n 3

echo -e "\n[*] Infrastructure Load:"
uptime | awk '{print "  Load Average: " $10 $11 $12}'
echo "============================================================"
