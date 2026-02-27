from flask import Flask, render_template, jsonify
import json
import os
import re

app = Flask(__name__, template_folder='../templates')
LOG_FILE = "logs/hell_activity.log"

def parse_logs():
    stats = {
        "total_data": 0, "total_time": 0, 
        "actors": {}, "countries": {}, 
        "recent_events": [], "hits": 0,
        "historical_ips": set(),
        "active_ips": set(),
        "attack_types": {},
        "signatures": {}
    }
    if not os.path.exists(LOG_FILE): return stats
    
    try:
        # Solo leemos las últimas 5000 líneas para no matar el CPU
        with open(LOG_FILE, "rb") as f:
            f.seek(0, os.SEEK_END)
            filesize = f.tell()
            # Leer aproximadamente los últimos 500KB del log
            offset = max(0, filesize - 500000)
            f.seek(offset)
            content = f.read().decode('utf-8', errors='ignore')
            
            # Extraer daño total (Injected MB)
            data_matches = re.findall(r"Data: ([\d.]+)MB", content)
            stats["total_data"] = sum(float(d) for d in data_matches)
            
            # Extraer tiempo total (Retention seconds)
            time_matches = re.findall(r"Time Lost: ([\d.]+)s", content)
            stats["total_time"] = sum(float(t) for t in time_matches)
            
            # Contador de impactos
            stats["hits"] = len(re.findall(r"TRIGGERED:", content))
            
            # IPs Históricas
            ips = re.findall(r"IP: ([\d.]+)", content)
            stats["historical_ips"] = list(set(ips))
            
            # Firmas y Clasificación
            signatures = re.findall(r"Classification: (.*?) \(", content)
            for s in signatures:
                stats["signatures"][s] = stats["signatures"].get(s, 0) + 1
            
            # Tipos de Ataque (basado en puertos)
            ports = re.findall(r"Target Port: (\d+)", content)
            port_map = {
                "22": "SSH Brute Force",
                "445": "SMB Worm / Lateral Movement",
                "3306": "SQL Injection / DB Scan",
                "1433": "MSSQL Attack",
                "80": "Web Exploit",
                "443": "SSL/Web Exploit",
                "3389": "RDP Brute Force",
                "9200": "ElasticSearch Exploit",
                "33001": "Aspera Data Theft"
            }
            for p in ports:
                type_str = port_map.get(p, f"Custom Port {p} Scan")
                stats["attack_types"][type_str] = stats["attack_types"].get(type_str, 0) + 1

            # Perfiles de Actores
            actors = re.findall(r"Actor: (\w+)", content)
            for a in actors: stats["actors"][a] = stats["actors"].get(a, 0) + 1
            
            # Países
            origins = re.findall(r"Origin: (.*?),", content)
            for country in origins:
                stats["countries"][country] = stats["countries"].get(country, 0) + 1

            # Eventos Recientes (Últimos 10)
            matches = re.finditer(r"TRIGGERED: (.*?)\nIP: (.*?) \(.*?\)\nOrigin: (.*?)\nNetwork: (.*?)\nClassification: (.*?)\nTarget Port: (.*?)\s\|", content, re.MULTILINE)
            for m in list(matches)[-10:]:
                stats["recent_events"].append({
                    "time": m.group(1),
                    "ip": m.group(2).strip(),
                    "origin": m.group(3).strip(),
                    "network": m.group(4).strip(),
                    "actor": m.group(5).strip(),
                    "port": m.group(6).strip()
                })
    except: pass
    
    # Simular IPs activas (últimas detectadas en los últimos 5 min)
    stats["active_ips"] = list(set([e['ip'] for e in stats["recent_events"]]))
    stats["new_ips_count"] = len(stats["historical_ips"])
    
    # Calcular TOPs
    if ips:
        stats["top_attacker"] = max(set(ips), key=ips.count)
    else:
        stats["top_attacker"] = "N/A"
        
    if stats["attack_types"]:
        stats["top_type"] = max(stats["attack_types"], key=stats["attack_types"].get)
    else:
        stats["top_type"] = "N/A"
        
    if ports:
        stats["top_port"] = max(set(ports), key=ports.count)
    else:
        stats["top_port"] = "N/A"
    
    return stats

@app.route('/')
def index(): return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats(): return jsonify(parse_logs())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)
