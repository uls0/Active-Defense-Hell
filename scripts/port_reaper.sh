#!/bin/bash

echo "[!] INICIANDO PORT REAPER..."

# Puertos a limpiar
TARGET_PORTS=(21 22 23 25 53 80 81 88 110 111 135 137 139 143 161 179 389 443 445 502 1433 3306 3389 6443 8080 2375 2376 9100 9090 9200 5601 6379 11211 8081 3000 5000 8000 11434 6666 8888)

for port in "${TARGET_PORTS[@]}"; do
    fuser -k $port/tcp 2>/dev/null
done

echo "[!] LEYENDO IPTABLES PARA EL VOID (20101-65535)..."
# Limpiar reglas previas del void
iptables -t nat -D PREROUTING -p tcp --dport 20101:65535 -j REDIRECT --to-ports 6666 2>/dev/null

# Aplicar redirección
iptables -t nat -A PREROUTING -p tcp --dport 20101:65535 -j REDIRECT --to-ports 6666

echo "[✔] SISTEMA LISTO PARA DESPLIEGUE SECUENCIAL"
