import requests
import json
import re
import os
from datetime import datetime

ISMALICIOUS_API_KEY = "b0959d3e-97c6-451f-9f95-5148c2da7ddd"
LOG_FILE = "../logs/hell_activity.log"
REPORT_FILE = "../logs/threat_intelligence_report.json"

def get_trending_ports():
    """Obtiene los puertos más atacados actualmente (SANS Internet Storm Center)"""
    print(f"[{datetime.now()}] 📡 Consultando radares globales de Threat Intelligence...")
    try:
        # API pública de SANS ISC para el Top 10 de puertos atacados hoy
        response = requests.get("https://isc.sans.edu/api/top10?json", timeout=10)
        if response.status_code == 200:
            data = response.json()
            trending_ports = [int(item['targetport']) for item in data]
            print(f"[{datetime.now()}] 🔥 Puertos en tendencia hoy: {trending_ports}")
            return trending_ports
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error consultando radares: {e}")
    return []

def extract_top_attackers():
    """Lee el log de HELL y extrae las IPs más agresivas de los últimos días"""
    ips = set()
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            # Regex simple para extraer IPs
            found_ips = re.findall(r'[0-9]+(?:\.[0-9]+){3}', content)
            for ip in found_ips:
                if ip not in ["127.0.0.1", "0.0.0.0"]:
                    ips.add(ip)
    except FileNotFoundError:
        pass
    return list(ips)[:5] # Tomamos un sample de 5 para no saturar la API

def analyze_with_ismalicious(ip):
    """Usa la API proporcionada para perfilar al atacante"""
    try:
        response = requests.post(
            "https://api.ismalicious.com/v1/check",
            headers={
                "Authorization": f"Bearer {ISMALICIOUS_API_KEY}",
                "Content-Type": "application/json"
            },
            json={"query": ip},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error con ismalicious.com en IP {ip}: {e}")
    return {"status": "error"}

def generate_threat_report():
    print("="*60)
    print(" 👁️ HELL MODULE: THREAT INTELLIGENCE & PORT ADAPTATION")
    print("="*60)
    
    trending = get_trending_ports()
    attackers = extract_top_attackers()
    
    report = {
        "timestamp": str(datetime.now()),
        "global_trending_ports": trending,
        "local_attackers_analysis": {}
    }
    
    print(f"[{datetime.now()}] 🧠 Analizando el perfil de {len(attackers)} atacantes recientes...")
    for ip in attackers:
        intel = analyze_with_ismalicious(ip)
        report["local_attackers_analysis"][ip] = intel
        time.sleep(1) # Rate limit respect
        
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
        
    print(f"[{datetime.now()}] ✅ Reporte generado en {REPORT_FILE}")
    
    if trending:
        print(f"
[💡] SUGERENCIA DE MUTACIÓN HELL:")
        print(f"El radar indica ataques masivos en los puertos: {trending[:3]}.")
        print("El sistema principal de HELL puede ser configurado para abrir estos puertos dinámicamente en el próximo ciclo.")

if __name__ == "__main__":
    generate_threat_report()
