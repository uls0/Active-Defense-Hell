#!/bin/sh
echo "[*] HELL OS ENTRYPOINT STARTING..."
echo "[*] Checking Network Privileges..."
ip addr show > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[❌] FATAL: No network privileges. Ensure 'cap_add: NET_ADMIN' is in docker-compose."
    exit 1
fi

echo "[*] Environment Ready. Launching HELL CORE..."
# Ejecutamos python con salida sin buffer
exec python3 -u hell_core.py
