#!/bin/bash

# ============================================================
# HELL TITAN FORENSIC CHECKER - v16.5.2 (ASCII EDITION)
# ============================================================

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
NC='\033[0m'

echo -e "${RED}============================================================${NC}"
echo -e "${WHITE}      HELL TITAN FORENSIC REPORT | MARCH 2026${NC}"
echo -e "${RED}============================================================${NC}"

# 1. ESTADO DE DOCKER
echo -e "${BLUE}[*] INFRAESTRUCTURA CORE:${NC}"
DOCKER_STATUS=$(docker ps --format "table {{.Names}}\t{{.Status}}" | grep hell)
if [ -z "$DOCKER_STATUS" ]; then
    echo -e "  [!!] Nucleo Docker: CAIDO"
else
    echo -e "  [OK] Nucleo Docker: ACTIVO"
    echo "$DOCKER_STATUS"
fi

# 2. METRICAS DE LOGS
LOG_FILE="/root/Active-Defense-Hell/logs/hell_activity.log"
if [ -f "$LOG_FILE" ]; then
    HITS=$(grep -c "\[HIT\]" "$LOG_FILE")
    BOMBS=$(grep -c "BOMB_DEPLOYED" "$LOG_FILE")
    TARPITS=$(grep -c "TARPIT_STALL" "$LOG_FILE")
    LETHAL=$(grep -c "LETHAL_EXIT" "$LOG_FILE")
    VOID_PKTS=$(grep -c "TRAPPED IN THE ABYSS" "$LOG_FILE")
    
    echo -e "\n${YELLOW}[*] METRICAS DE COMBATE RECIENTES:${NC}"
    echo -e "  [STATS] Total de Ataques (Hits): ${GREEN}$HITS${NC}"
    echo -e "  [BOMB]  Bombas Fifield Enviadas: ${GREEN}$BOMBS${NC}"
    echo -e "  [TARPIT] Bots en Tarpit (Greasy): ${GREEN}$TARPITS${NC}"
    echo -e "  [LETHAL] Bots Eliminados (Lethal): ${GREEN}$LETHAL${NC}"
    echo -e "  [VOID]   Capturas en el Abismo:    ${GREEN}$VOID_PKTS${NC}"
else
    echo -e "\n${RED}[!] Error: Archivo de logs no encontrado.${NC}"
fi

# 3. ESTADO DE PUERTOS (TOP 100)
echo -e "\n${CYAN}[*] ESTADO DE PUERTOS DE ENGANO:${NC}"
PORT_LIST=(21 22 23 25 53 80 81 88 110 111 135 137 139 143 161 179 389 443 445 449 502 102 995 1433 1521 1883 2121 2222 2323 2375 3306 3389 4455 5678 8080 8081 8082 8090 8443 8888 9200 33001 1338 8545 3333 18080 20000 47808 6160 6666 65535)

OPEN_COUNT=0
for port in "${PORT_LIST[@]}"; do
    if netstat -tulpn | grep -q ":$port "; then
        ((OPEN_COUNT++))
    fi
done

echo -e "  [INFO] Resumen de Trampas: ${GREEN}$OPEN_COUNT/${#PORT_LIST[@]}${NC} puertos LISTOS."
if [ $OPEN_COUNT -lt ${#PORT_LIST[@]} ]; then
    echo -e "  [WARN] Advertencia: Algunos puertos criticos estan cerrados."
fi

# 4. TOP ADVERSARIOS
echo -e "\n${PURPLE}[*] TOP 5 ADVERSARIOS (IP):${NC}"
if [ -f "$LOG_FILE" ]; then
    grep "IP:" "$LOG_FILE" | awk -F'|' '{print $2}' | sort | uniq -c | sort -nr | head -n 5
fi

echo -e "${RED}============================================================${NC}"
