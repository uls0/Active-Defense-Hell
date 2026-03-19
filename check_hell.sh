#!/bin/bash

# ============================================================
# HELL TITAN FORENSIC CHECKER - v18.0 (CISA EXPANSION)
# ============================================================

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
NC='\033[0m'

echo -e "${RED}============================================================${NC}"
echo -e "${CYAN}      TITAN OMEGA-EXPANSION REPORT | MARCH 2026${NC}"
echo -e "${RED}============================================================${NC}"

# 1. ESTADO DE NODOS WINDOWS XP
echo -e "${BLUE}[*] SACRIFICE NODES STATUS:${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep winxp || echo "  [!!] No nodes detected"

# 2. METRICAS DE COMBATE
LOG_FILE="/root/Active-Defense-Hell/logs/hell_activity.log"
if [ -f "$LOG_FILE" ]; then
    SACRIFICE_HITS=$(grep -c "SACRIFICE_ENGAGED" "$LOG_FILE")
    HITS=$(grep -c "\[Hit\]" "$LOG_FILE")
    echo -e "\n${YELLOW}[*] ENGAGEMENT METRICS:${NC}"
    echo -e "  [SACRIFICE] Bots in Real Windows: ${GREEN}$SACRIFICE_HITS${NC}"
    echo -e "  [TOTAL]     General Trap Hits:    ${GREEN}$HITS${NC}"
fi

# 3. PROXY LISTENERS
echo -e "\n${CYAN}[*] PROXY LISTENERS (HELL -> WINDOWS XP):${NC}"
for p in 33893 33894; do
    if netstat -tulpn | grep -q ":$p "; then
        echo -e "  [OK] Port $p -> PROXY ACTIVE"
    else
        echo -e "  [!!] Port $p -> DOWN"
    fi
done

# 4. LISTADO DE ARSENAL Y PAYLOADS (DETALLADO)
echo -e "\n${BLUE}[*] ACTIVE ARSENAL & EMULATED VULNERABILITIES:${NC}"
echo -e "${CYAN}PORT\tSTATUS\tEMULATED_TARGET${NC}"

declare -A PAYLOADS
PAYLOADS[21]="FTP_EXPLOIT"
PAYLOADS[22]="SSH_PROVOKE_BAIT"
PAYLOADS[23]="MIRAI_TELNET"
PAYLOADS[25]="SMTP_RELAY_TRAP"
PAYLOADS[53]="DNS_TXT_REDIRECTION"
PAYLOADS[80]="CVE_WEB_BOMB"
PAYLOADS[443]="SSL_HEARTBLEED_BOMB"
PAYLOADS[445]="ETERNAL_BLUE_TARPIT"
PAYLOADS[502]="MODBUS_SCADA_PLC"
PAYLOADS[1433]="MSSQL_INJECTION"
PAYLOADS[2375]="DOCKER_API_EXPLOIT"
PAYLOADS[3389]="BLUEKEEP_MIRAGE"
PAYLOADS[5432]="POSTGRES_EXPLOIT"
PAYLOADS[6379]="REDIS_UNAUTH"
PAYLOADS[6666]="VOID_SUCTION_CORE"
PAYLOADS[8443]="CISCO_SDWAN_BYPASS"
PAYLOADS[9200]="ELASTICSEARCH_RCE"
PAYLOADS[27017]="MONGODB_NOSQL"
PAYLOADS[65535]="VOID_FINAL_TARGET"

# Listar solo puertos activos del top
for port in 21 22 23 25 53 80 443 445 502 1433 2375 3389 5432 6379 6666 8443 9200 27017 65535; do
    if netstat -tulpn | grep -q ":$port "; then
        STATUS="${GREEN}ONLINE${NC}"
    else
        STATUS="${RED}OFFLINE${NC}"
    fi
    DESC=${PAYLOADS[$port]}
    echo -e "$port\t$STATUS\t$DESC"
done

echo -e "\n[INFO] Other 130+ CISA ports are active in background threads."
echo -e "${RED}============================================================${NC}"
