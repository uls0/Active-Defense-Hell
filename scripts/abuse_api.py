import requests
import json
import os
import time
from datetime import datetime

API_KEY = "a294ad97c828dc6f8e5111d0209475ddbb3e984672d651688d3e3f9007c6a17520f2d20dc46974db"
REPORT_DB = "logs/reported_ips.json"
DAILY_LIMIT = 100

def load_reported_db():
    if os.path.exists(REPORT_DB):
        with open(REPORT_DB, "r") as f:
            return json.load(f)
    return {"total_reports": 0, "last_reset": str(datetime.now().date()), "ips": {}}

def save_reported_db(db):
    with open(REPORT_DB, "w") as f:
        json.dump(db, f, indent=4)

def report_ip(ip, categories, comment):
    db = load_reported_db()
    
    # Resetear contador si es un nuevo día
    today = str(datetime.now().date())
    if db["last_reset"] != today:
        db["total_reports"] = 0
        db["last_reset"] = today

    # Verificar límites
    if db["total_reports"] >= DAILY_LIMIT:
        print(f"[!] Límite de reportes diarios alcanzado ({DAILY_LIMIT}). IP {ip} en espera.")
        return False

    if ip in db["ips"] and db["ips"][ip] == today:
        return False # Ya reportada hoy

    url = 'https://api.abuseipdb.com/api/v2/report'
    params = {
        'ip': ip,
        'categories': categories,
        'comment': comment
    }
    headers = {
        'Accept': 'application/json',
        'Key': API_KEY
    }

    try:
        response = requests.post(url, data=params, headers=headers)
        if response.status_code == 200:
            db["total_reports"] += 1
            db["ips"][ip] = today
            save_reported_db(db)
            print(f"[✔] IP {ip} reportada exitosamente a AbuseIPDB. Total hoy: {db['total_reports']}")
            return True
        else:
            print(f"[❌] Error reportando IP {ip}: {response.text}")
            return False
    except Exception as e:
        print(f"[!] Error de conexión con AbuseIPDB: {e}")
        return False
