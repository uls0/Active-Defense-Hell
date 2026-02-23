import requests
import json
import re
import os
import time
from datetime import datetime

ISMALICIOUS_API_KEY = "b0959d3e-97c6-451f-9f95-5148c2da7ddd"
LOG_FILE = "logs/hell_activity.log"
REPORT_FILE = "logs/threat_intelligence_report.json"

def get_trending_ports():
    print(f"[{datetime.now()}] 📡 Consultando radares globales...")
    try:
        response = requests.get("https://isc.sans.edu/api/top10?json", timeout=10)
        if response.status_code == 200:
            data = response.json()
            trending = [int(item['targetport']) for item in data]
            print(f"🔥 Puertos en tendencia: {trending}")
            return trending
    except: pass
    return []

def extract_attackers():
    ips = set()
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                found_ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', content)
                for ip in found_ips:
                    if ip not in ["127.0.0.1", "0.0.0.0"]: ips.add(ip)
    except: pass
    return list(ips)[:5]

def analyze_ip(ip):
    try:
        response = requests.post(
            "https://api.ismalicious.com/v1/check",
            headers={"Authorization": f"Bearer {ISMALICIOUS_API_KEY}", "Content-Type": "application/json"},
            json={"query": ip},
            timeout=10
        )
        return response.json() if response.status_code == 200 else {"status": "error"}
    except: return {"status": "error"}

def run():
    print("="*60)
    print(" 👁️ HELL MODULE: THREAT INTELLIGENCE")
    print("="*60)
    
    trending = get_trending_ports()
    attackers = extract_attackers()
    
    report = {
        "timestamp": str(datetime.now()),
        "trending": trending,
        "analysis": {ip: analyze_ip(ip) for ip in attackers}
    }
    
    os.makedirs("logs", exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
        
    print(f"✅ Reporte generado en {REPORT_FILE}")
    if trending:
        msg = f"\n[💡] SUGERENCIA: Los puertos {trending[:3]} están bajo ataque global. Considera abrirlos en HELL."
        print(msg)

if __name__ == "__main__":
    run()
