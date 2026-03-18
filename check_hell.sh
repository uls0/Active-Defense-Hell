#!/bin/bash
# ============================================================
#      🔍 HELL TITAN v16.2: COMMAND DASHBOARD
# ============================================================
BASE_DIR="/root/Active-Defense-Hell"
LOG_FILE="$BASE_DIR/logs/hell_activity.log"

echo -e "\e[1;31m============================================================\e[0m"
echo -e "\e[1;37m      ☢️  HELL TITAN FORENSIC REPORT | MARCH 2026\e[0m"
echo -e "\e[1;31m============================================================\e[0m"

# 1. Estado de Infraestructura
echo -e "\n\e[1;34m[*] INFRAESTRUCTURA CORE:\e[0m"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep hell || echo "  [!] Docker no detectado o caido."
PROCESS_CORE=$(ps aux | grep -E 'hell_core|hell_reborn' | grep -v grep | wc -l)
if [ $PROCESS_CORE -gt 0 ]; then
    echo -e "  [✅] Núcleo Python Host: ACTIVO (PID: $(pgrep -f hell))"
else
    echo -e "  [❌] Núcleo Python Host: CAÍDO"
fi

# 2. Resumen de Combate (Parsing de Logs)
echo -e "\n\e[1;33m[*] MÉTRICAS DE COMBATE RECIENTES:\e[0m"
if [ -f "$LOG_FILE" ]; then
    BOMBS=$(grep -c "\[BOMB_DEPLOYED\]" "$LOG_FILE")
    TARPITS=$(grep -c "\[TARPIT_STALL\]" "$LOG_FILE")
    KILLED=$(grep -c "\[LETHAL_EXIT\]" "$LOG_FILE")
    RDP_SESS=$(grep -c "\[MIRAGE_ENGAGED\]" "$LOG_FILE")
    VOID_HITS=$(grep -c "TRAPPED IN THE ABYSS" "$LOG_FILE")

    echo -e "  [💣] Bombas Fifield Enviadas: \e[1;32m$BOMBS\e[0m"
    echo -e "  [🍯] Bots en Tarpit (Greasy): \e[1;32m$TARPITS\e[0m"
    echo -e "  [💀] Bots Eliminados (Lethal): \e[1;32m$KILLED\e[0m"
    echo -e "  [🪤] Espejismos RDP Activos:  \e[1;32m$RDP_SESS\e[0m"
    echo -e "  [🌌] Capturas en el VOID:     \e[1;32m$VOID_HITS\e[0m"
else
    echo "  [!] Log no encontrado en $LOG_FILE"
fi

# 3. Puertos Críticos (Live Check)
echo -e "\n\e[1;36m[*] ESTADO DE PUERTOS DE ENGAÑO:\e[0m"
for port in 80 443 445 3389 5678 8443 6666 65535; do
    (echo > /dev/tcp/127.0.0.1/$port) >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "  [✅] Port $port: \e[1;32mOPEN\e[0m"
    else
        echo -e "  [❌] Port $port: \e[1;31mCLOSED\e[0m"
    fi
done

# 4. Top de Atacantes
echo -e "\n\e[1;35m[*] TOP 5 ADVERSARIOS (ASN/IP):\e[0m"
if [ -f "$LOG_FILE" ]; then
    grep "IP:" "$LOG_FILE" | awk '{print $6}' | sort | uniq -c | sort -nr | head -n 5
else
    echo "  [!] No hay datos forenses."
fi

echo -e "\e[1;31m============================================================\e[0m"
