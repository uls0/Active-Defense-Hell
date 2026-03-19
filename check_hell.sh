#!/bin/bash

# ============================================================
# HELL TITAN FORENSIC CHECKER - v17.3 (LIGHT EDITION)
# ============================================================

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
NC='\033[0m'

echo -e "${RED}============================================================${NC}"
echo -e "${CYAN}      TITAN LIGHT SACRIFICE GRID REPORT | MARCH 2026${NC}"
echo -e "${RED}============================================================${NC}"

# 1. ESTADO DE NODOS WINDOWS XP
echo -e "${BLUE}[*] LIGHT SACRIFICE NODES STATUS:${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep winxp

# 2. METRICAS
LOG_FILE="/root/Active-Defense-Hell/logs/hell_activity.log"
if [ -f "$LOG_FILE" ]; then
    SACRIFICE_HITS=$(grep -c "SACRIFICE_ENGAGED" "$LOG_FILE")
    echo -e "\n${YELLOW}[*] ENGAGEMENT METRICS:${NC}"
    echo -e "  [SACRIFICE] Bots in WinXP: ${GREEN}$SACRIFICE_HITS${NC}"
    echo -e "  [TOTAL]     General Hits: ${GREEN}$(grep -c "\[Hit\]" "$LOG_FILE")${NC}"
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

echo -e "\n${RED}============================================================${NC}"
