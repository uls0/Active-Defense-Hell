import os
import re
import sys
from abuse_api import report_ip

LOG_FILE = "logs/hell_activity.log"

def analyze_and_report():
    if not os.path.exists(LOG_FILE):
        print("[!] Log no encontrado.")
        return

    print("[*] Iniciando proceso de reporte diario a AbuseIPDB...")
    
    # Extraer IPs y sus estadísticas del log
    with open(LOG_FILE, "r", encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Patrón para encontrar bloques de engagement
    # IP: (.*?) \(.*\)
Origin: (.*?) \| Profile: (.*)
Network: (.*)
Classification: (.*)
Target Port: (\d+) \| Hit Count: (\d+)
    matches = re.finditer(r"IP: ([\d.]+) \(.*?\)
Origin: (.*?)
Network: (.*?)
Classification: (.*?) \(.*?\)
Target Port: (\d+) \| Hit Count: (\d+)", content)
    
    candidates = {}
    for m in matches:
        ip = m.group(1)
        origin = m.group(2)
        network = m.group(3)
        actor = m.group(4)
        port = m.group(5)
        hits = int(m.group(6))
        
        if ip not in candidates:
            candidates[ip] = {"hits": hits, "port": port, "actor": actor, "origin": origin}
        else:
            if hits > candidates[ip]["hits"]:
                candidates[ip]["hits"] = hits

    # Ordenar por agresividad (Hits)
    sorted_ips = sorted(candidates.items(), key=lambda x: x[1]['hits'], reverse=True)
    
    reported_count = 0
    for ip, data in sorted_ips:
        if reported_count >= 100: break
        
        # Categorías AbuseIPDB: 14 (Port Scan), 18 (Brute-Force), 15 (Hacking/SMB), 21 (Proxy)
        cat = "14"
        if data["port"] in ["22", "3389"]: cat = "18,14"
        if data["port"] in ["445", "4455"]: cat = "15,14"
        
        comment = f"HELL ACTIVE DEFENSE: Bot detected on port {data['port']} with {data['hits']} hits. Classification: {data['actor']}. Origin: {data['origin']}. Total resources exhausted successfully."
        
        if report_ip(ip, cat, comment):
            reported_count += 1

    print(f"[*] Proceso finalizado. IPs procesadas: {reported_count}")

if __name__ == "__main__":
    analyze_and_report()
