#!/bin/bash
echo "============================================================"
echo "      🔍 HELL INFRASTRUCTURE PRE-FLIGHT CHECK"
echo "============================================================"

echo "[*] Checking Docker Containers..."
docker ps --format "table {{.Names}}	{{.Status}}	{{.Ports}}" | grep hell

echo -e "
[*] Checking Network Listeners (Host Mode)..."
# Verificamos si los puertos clave están abiertos
for port in 80 445 3306 8888 2222; do
    netstat -tuln | grep ":$port " > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "  [✅] Port $port is OPEN and LISTENING."
    else
        echo -e "  [❌] Port $port is CLOSED."
    fi
done

echo -e "
[*] Checking Log Activity (Last 5 lines)..."
tail -n 5 logs/hell_activity.log

echo -e "
[*] System Resources..."
free -h | grep Mem

echo "============================================================"
