import time
import os
import requests
import json
import threading
from collections import Counter

# --- CONFIGURACIÓN ---
ABUSE_KEY = "a294ad97c828dc6f8e5111d0209475ddbb3e984672d651688d3e3f9007c6a17520f2d20dc46974db"
VT_KEY = "cf71ef8287e23566adc72ef2a5c519f0f542e66bfdacfcfc1ca3660fb5662279"
LOG_FILE = "/root/Active-Defense-Hell/logs/hell_activity.log"
REPORT_DB = "/root/Active-Defense-Hell/logs/reported_ips.json"

# Condiciones
HIT_THRESHOLD = 15 # Reportar tras 15 hits
ELITE_PORTS = ["6443", "8080", "2375", "2376", "9200", "6379", "8081", "8000"]

# Estado en memoria
ip_counters = Counter()
reported_cache = set()

def load_reported():
    global reported_cache
    if os.path.exists(REPORT_DB):
        try:
            with open(REPORT_DB, "r") as f:
                data = json.load(f)
                reported_cache = set(data.get("ips", {}).keys())
        except: pass

def save_reported(ip):
    global reported_cache
    reported_cache.add(ip)
    db = {"ips": {ip: str(time.time()) for ip in reported_cache}}
    with open(REPORT_DB, "w") as f:
        json.dump(db, f)

def report_to_abuseipdb(ip, port, hits):
    url = 'https://api.abuseipdb.com/api/v2/report'
    comment = f"HELL STORM: Aggressive bot detected on port {port}. Total hits: {hits}. Identity: MexCapital Financial Honey-Node. High confidence botnet/scanner."
    params = {'ip': ip, 'categories': '14,18,19', 'comment': comment}
    headers = {'Accept': 'application/json', 'Key': ABUSE_KEY}
    try:
        res = requests.post(url, data=params, headers=headers, timeout=10)
        return res.status_code == 200
    except: return False

def report_to_virustotal(ip, port):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}/comments"
    comment = f"MEXCAPITAL-DEFENSE: Critical engagement on financial api port {port}. Confirmed malicious actor captured by HELL v17.4 native."
    headers = {"x-apikey": VT_KEY, "Content-Type": "application/json"}
    payload = {"data": {"type": "comment", "attributes": {"text": comment}}}
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        return res.status_code in [200, 201]
    except: return False

def process_line(line):
    # Formato esperado: [Hit] 2026-03-24 11:15:58 | IP: 154.208.49.149 | Port: 445 | ...
    try:
        if "IP:" not in line or "Port:" not in line: return
        parts = line.split("|")
        ip = parts[1].replace("IP:", "").strip()
        port = parts[2].replace("Port:", "").strip()
        
        if ip in reported_cache: return

        ip_counters[ip] += 1
        
        # Disparadores de reporte inmediato
        should_report = False
        if ip_counters[ip] >= HIT_THRESHOLD: should_report = True
        if port in ELITE_PORTS: should_report = True
        
        if should_report:
            print(f"[!] CONDICIÓN CUMPLIDA: Reportando {ip} (Puerto: {port}, Hits: {ip_counters[ip]})")
            success_abuse = report_to_abuseipdb(ip, port, ip_counters[ip])
            success_vt = report_to_virustotal(ip, port)
            
            if success_abuse or success_vt:
                save_reported(ip)
                print(f"[✔] IP {ip} neutralizada reputacionalmente.")
    except: pass

def monitor_logs():
    load_reported()
    print("[*] THREAT_INTEL_AUTO: Monitoring hell_activity.log...")
    
    # Abrir archivo y mover al final
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'a').close()
        
    with open(LOG_FILE, "r") as f:
        f.seek(0, 2) # Ir al final
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            process_line(line)

if __name__ == "__main__":
    monitor_logs()
