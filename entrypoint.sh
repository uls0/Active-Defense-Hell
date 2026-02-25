#!/bin/sh
echo "[*] HELL OS ENTRYPOINT STARTING..."

# 1. Limpieza de procesos colgados (Zombies)
echo "[*] Purging legacy HELL processes..."
pkill -9 python3 > /dev/null 2>&1
pkill -9 python > /dev/null 2>&1

# 2. Verificación de privilegios de red
echo "[*] Checking Network Privileges..."
ip addr show > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[❌] FATAL: No network privileges. Ensure 'privileged: true' is in docker-compose."
    exit 1
fi

# 3. Diagnóstico de puertos ocupados (Netstat alternativo)
echo "[*] Port Status Scan:"
for port in 80 443 445 3306 2222 8888; do
    (echo > /dev/tcp/127.0.0.1/$port) >/dev/null 2>&1 && echo "  [!] Warning: Port $port is ALREADY OCCUPIED." || echo "  [+] Port $port is free."
done

echo "[*] Environment Ready. Launching HELL CORE v9.1.4..."
exec python3 -u hell_core.py
