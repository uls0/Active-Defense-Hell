import sys
import os
import time
import re
from datetime import datetime, timedelta

# Asegurar que los scripts del proyecto sean importables
sys.path.append(os.path.join(os.getcwd(), 'scripts'))
import abuse_api
import threat_intel

LOG_FILE = "logs/hell_activity.log"
VT_KEY = os.getenv("VT_API_KEY", "")
ABUSE_KEY = os.getenv("ABUSEIPDB_API_KEY", "")

def get_recent_attackers(hours=10):
    """Analiza el log en busca de IPs activas en las ultimas X horas."""
    if not os.path.exists(LOG_FILE):
        return {}
    
    attackers = {}
    time_threshold = datetime.now() - timedelta(hours=hours)
    
    # Expresiones regulares para capturar IP y Timestamp
    # [+] ULTIMATE DECEPTION TRIGGERED: 2026-02-27 18:52:56
    # IP: 204.76.203.56
    
    with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Bloques de disparos
    blocks = re.split(r"----------------------------------------", content)
    
    for block in blocks:
        ts_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", block)
        ip_match = re.search(r"IP: ([\d\.]+)", block)
        port_match = re.search(r"Target Port: (\d+)", block)
        botnet_match = re.search(r"â˜¢ï¸ ([\w\-]+)", block)
        
        if ts_match and ip_match:
            ts = datetime.strptime(ts_match.group(1), '%Y-%m-%d %H:%M:%S')
            if ts > time_threshold:
                ip = ip_match.group(1)
                port = port_match.group(1) if port_match else "Unknown"
                botnet = botnet_match.group(1) if botnet_match else None
                
                if ip not in attackers:
                    attackers[ip] = {'hits': 0, 'ports': set(), 'botnet': botnet}
                
                attackers[ip]['hits'] += 1
                attackers[ip]['ports'].add(port)
                if botnet: attackers[ip]['botnet'] = botnet

    return attackers

def run_batch_report():
    print(f"[*] Iniciando Reporte en Lote (Ultimas 10 horas) - {datetime.now()}")
    attackers = get_recent_attackers(10)
    
    if not attackers:
        print("[i] No se detectaron atacantes nuevos en el rango de tiempo.")
        return

    count = 0
    for ip, data in attackers.items():
        # Criterio: Mas de 5 hits o botnet identificada
        if data['hits'] > 5 or data['botnet']:
            ports_str = ", ".join(list(data['ports']))
            botnet_info = f" identified as {data['botnet']}" if data['botnet'] else ""
            comment = f"HELL BATCH REPORT: Persistent attacker detected{botnet_info}. Target Ports: {ports_str}. Hit Count: {data['hits']} in last 10h."
            
            print(f"[>] Reportando {ip} ({data['hits']} hits)...")
            
            # 1. AbuseIPDB
            abuse_api.report_ip(ip, "14,15", comment)
            
            # 2. VirusTotal
            threat_intel.report_ip_to_vt(ip, VT_KEY, comment)
            
            count += 1
            time.sleep(1) # Evitar saturar rate limits locales
    
    print(f"[✅] Lote finalizado. Total IPs reportadas: {count}")

if __name__ == "__main__":
    run_batch_report()
