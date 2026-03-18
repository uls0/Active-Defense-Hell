#!/bin/bash
set -e

echo "[*] HELL OS ENTRYPOINT STARTING..."

# Limpiar reglas previas del VOID
iptables -t nat -F PREROUTING || true

# Configurar el VOID (Redirigir rango masivo al 6666)
echo "[*] ACTIVATING VOID REDIRECTION (20101-65534 -> 6666)"
iptables -t nat -A PREROUTING -p tcp --dport 20101:65534 -j REDIRECT --to-ports 6666

echo "[*] Network Privileges Granted. Starting Core..."
exec "$@"
