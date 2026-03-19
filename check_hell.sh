#!/bin/bash

# ============================================================
# HELL TITAN FORENSIC CHECKER - v17.2 (SACRIFICE EDITION)
# ============================================================

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
CYAN='\033[1;36m'
NC='\033[0m'

echo -e "${RED}============================================================${NC}"
echo -e "${CYAN}      TITAN SACRIFICE GRID REPORT | MARCH 2026${NC}"
echo -e "${RED}============================================================${NC}"

# 1. ESTADO DE NODOS WINDOWS
echo -e "${BLUE}[*] SACRIFICE NODES STATUS:${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep win

# 2. METRICAS DE INTERCEPTACION
LOG_FILE="/root/Active-Defense-Hell/logs/hell_activity.log"
if [ -f "$LOG_FILE" ]; then
    SACRIFICE_HITS=$(grep -c "SACRIFICE_ENGAGED" "$LOG_FILE")
    echo -e "\n${YELLOW}[*] ENGAGEMENT METRICS:${NC}"
    echo -e "  [SACRIFICE] Bots trapped in Real Windows: ${GREEN}$SACRIFICE_HITS${NC}"
    echo -e "  [TOTAL]     General Trap Hits:           ${GREEN}$(grep -c "\[HIT\]" "$LOG_FILE")${NC}"
fi

# 3. VERIFICACION DE PUERTOS PROXY
echo -e "\n${CYAN}[*] PROXY LISTENERS (HELL -> WINDOWS):${NC}"
for p in 33891 33892 33893 33894; do
    if netstat -tulpn | grep -q ":$p "; then
        echo -e "  [OK] Port $p -> PROXY ACTIVE"
    else
        echo -e "  [!!] Port $p -> DOWN"
    fi
done

echo -e "\n${RED}============================================================${NC}"
