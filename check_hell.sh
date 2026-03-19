#!/bin/bash

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
NC='\033[0m'

echo -e "${RED}============================================================${NC}"
echo -e "${CYAN}      TITAN OMEGA-EXPANSION REPORT | MARCH 2026${NC}"
echo -e "${RED}============================================================${NC}"

# 1. NODOS XP
echo -e "${BLUE}[*] SACRIFICE NODES STATUS:${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep winxp || echo "  [!!] No nodes detected"

# 2. PROXY
echo -e "\n${CYAN}[*] PROXY LISTENERS:${NC}"
for p in 33893 33894; do
    if netstat -tulpn | grep -q ":$p "; then
        echo -e "  [OK] Port $p -> PROXY ACTIVE"
    else
        echo -e "  [!!] Port $p -> DOWN"
    fi
done

# 3. ARSENAL TABULAR
echo -e "\n${BLUE}[*] ACTIVE ARSENAL & PAYLOADS:${NC}"
printf "${CYAN}%-10s %-12s %-20s${NC}\n" "PORT" "STATUS" "EMULATED_TARGET"

declare -A PAYLOADS=( [21]="FTP_EXPLOIT" [22]="SSH_PROVOKE" [23]="MIRAI_TELNET" [25]="SMTP_TRAP" [53]="DNS_BAIT" [80]="WEB_BOMB" [443]="SSL_BOMB" [445]="SMB_TARPIT" [502]="PLC_MODBUS" [1433]="MSSQL_INJ" [2375]="DOCKER_API" [3389]="BLUEKEEP" [5432]="POSTGRES" [6379]="REDIS_UNAUTH" [6666]="VOID_CORE" [8443]="CISCO_BYPASS" [9200]="ELASTIC_RCE" [27017]="MONGODB" [65535]="VOID_FINAL" )

for port in 21 22 23 25 53 80 443 445 502 1433 2375 3389 5432 6379 6666 8443 9200 27017 65535; do
    if netstat -tulpn | grep -q ":$port "; then
        STATUS="ONLINE"
        COLOR=$GREEN
    else
        STATUS="OFFLINE"
        COLOR=$RED
    fi
    printf "%-10s ${COLOR}%-12s${NC} %-20s\n" "$port" "$STATUS" "${PAYLOADS[$port]}"
done

echo -e "\n${RED}============================================================${NC}"
