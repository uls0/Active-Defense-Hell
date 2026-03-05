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
        "signatures": {},
        "botnets": [],
        "vt_reports": 0,
        "abuse_reports": 0
    }
    if not os.path.exists(LOG_FILE): return stats
    
    try:
        # Solo leemos los últimos 5000 líneas para no matar el CPU
        with open(LOG_FILE, "rb") as f:
            f.seek(0, os.SEEK_END)
            filesize = f.tell()
            # Leer aproximadamente los últimos 1MB del log para más contexto
            offset = max(0, filesize - 1000000)
            f.seek(offset)
            content = f.read().decode('utf-8', errors='ignore')
            
            # Extraer daño total (Injected MB)
            data_matches = re.findall(r"Data: ([\d.]+)MB", content)
            stats["total_data"] = sum(float(d) for d in data_matches)
            
            # Extraer tiempo total (Retention seconds)
            time_matches = re.findall(r"Time Lost: ([\d.]+)s", content)
            stats["total_time"] = sum(float(t) for t in time_matches)
            
            # Contador de impactos
            stats["hits"] = len(re.findall(r"TRIGGERED:", content)) + len(re.findall(r"AETERNUM-DETECTION", content))
            
            # Reportes enviados (conteo de logs de reporte)
            stats["vt_reports"] = len(re.findall(r"reportada pÃºblicamente en VirusTotal", content))
            stats["abuse_reports"] = len(re.findall(r"reportada exitosamente a AbuseIPDB", content))
            
            # Detecciones de Botnets
            # [☢️ AETERNUM-DETECTION]: 2026-02-27 18:52:56
            botnet_matches = re.finditer(r"\[â˜¢ï¸ (.*?)\]: (.*?)\n.*?IP: ([\d\.]+)", content, re.MULTILINE)
            for bm in list(botnet_matches)[-5:]:
                stats["botnets"].append({
                    "name": bm.group(1).strip(),
                    "time": bm.group(2).strip(),
                    "ip": bm.group(3).strip()
                })

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
                "23": "Telnet Botnet (Mirai/Gafgyt)",
                "445": "SMB Worm / Lateral Movement",
                "3306": "SQL Injection / DB Scan",
                "1433": "MSSQL Attack",
                "80": "Web Exploit",
                "443": "SSL/Web Exploit",
                "3389": "RDP Brute Force",
                "9200": "ElasticSearch Exploit",
                "33001": "Aspera Data Theft",
                "8545": "Aeternum C2 (Ethereum)",
                "18080": "Aeternum C2 (Monero)",
                "11434": "Ollama AI Bait",
                "6443": "K8s API Exploit"
            }
            for p in ports:
                type_str = port_map.get(p, f"Custom Port {p} Scan")
                stats["attack_types"][type_str] = stats["attack_types"].get(type_str, 0) + 1

            # Países
            origins = re.findall(r"Origin: (.*?),", content)
            for country in origins:
                stats["countries"][country] = stats["countries"].get(country, 0) + 1

            # Eventos Recientes (Últimos 15 para el feed)
            matches = re.finditer(r"(?:TRIGGERED|AETERNUM-DETECTION): (.*?)\n----------------------------------------\nIP: (.*?) \(.*?\)\nOrigin: (.*?)\nNetwork: (.*?)\nClassification: (.*?)\nTarget Port: (.*?)\s\|", content, re.MULTILINE)
            for m in list(matches)[-15:]:
                stats["recent_events"].append({
                    "time": m.group(1),
                    "ip": m.group(2).strip(),
                    "origin": m.group(3).strip(),
                    "network": m.group(4).strip(),
                    "actor": m.group(5).strip(),
                    "port": m.group(6).strip()
                })
    except Exception as e:
        print(f"Error parseando logs: {e}")
    
    stats["active_ips"] = list(set([e['ip'] for e in stats["recent_events"]]))
    stats["new_ips_count"] = len(stats["historical_ips"])
    
    # TOP Metrics
    stats["top_attacker"] = max(set(ips), key=ips.count) if ips else "N/A"
    stats["top_type"] = max(stats["attack_types"], key=stats["attack_types"].get) if stats["attack_types"] else "N/A"
    stats["top_port"] = max(set(ports), key=ports.count) if ports else "N/A"
    
    return stats

@app.route('/')
def index(): return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats_api(): return jsonify(parse_logs())

@app.route('/v1/auth/verify/<token>')
def canary_trigger(token):
    """Captura la IP real de quien abra el archivo trampa."""
    real_ip = requests.remote_addr if not request.headers.get('X-Forwarded-For') else request.headers.get('X-Forwarded-For')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Log de captura de Administrador
    log_msg = f"\n[🎯 CANARY TRIGGERED]: {timestamp}\n----------------------------------------\nREAL OPERATOR IP DETECTED: {real_ip}\nToken ID: {token}\nStatus: EXPOSED\n----------------------------------------\n"
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(log_msg)
    
    # REPORTE AUTOMÁTICO INMEDIATO (Cazar al operador)
    import abuse_api
    import threat_intel
    comment = f"HELL ACTIVE DEFENSE: Identified REAL OPERATOR IP for a botnet. Attacker accessed a honey-credential from token {token}."
    abuse_api.report_ip(real_ip, "14", comment)
    threat_intel.report_ip_to_vt(real_ip, os.getenv("VT_API_KEY", ""), comment)
    
    return jsonify({"status": "error", "message": "Invalid credentials", "code": 403})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)
