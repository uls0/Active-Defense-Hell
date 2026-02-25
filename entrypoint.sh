#!/bin/sh
echo "[*] HELL OS ENTRYPOINT STARTING..."

# Eliminamos pkill para evitar matar otros módulos en modo host
echo "[*] Checking Network Privileges..."
ip addr show > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[❌] FATAL: No network privileges."
    exit 1
fi

echo "[*] Launching Task: $@"
exec "$@"
