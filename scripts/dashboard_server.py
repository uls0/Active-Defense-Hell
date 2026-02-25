from flask import Flask, render_template, jsonify
import json
import os
import re
import subprocess

app = Flask(__name__, template_folder='../templates')
LOG_FILE = "logs/hell_activity.log"
INTEL_FILE = "logs/mesh_intel.json"

def get_kernel_blocks():
    """Extrae las IPs bloqueadas por Iptables en el host"""
    try:
        result = subprocess.run(["sudo", "iptables", "-L", "INPUT", "-n"], capture_output=True, text=True)
        blocks = re.findall(r"DROP\s+all\s+--\s+([\d\.]+)", result.stdout)
        return list(set(blocks))
    except: return []

def parse_logs():
    stats = {
        "total_data": 0, "total_time": 0, 
        "actors": {}, "countries": {}, 
        "recent_events": [], "kernel_blocks": get_kernel_blocks()
    }
    if not os.path.exists(LOG_FILE): return stats
    
    with open(LOG_FILE, "r", encoding='utf-8', errors='ignore') as f:
        content = f.read()
        stats["total_data"] = sum(float(d) for d in re.findall(r"Injected: ([\d.]+)MB", content))
        stats["total_time"] = sum(float(t) for t in re.findall(r"Time Lost: ([\d.]+)s", content))
        
        # Parsear Actores
        actors = re.findall(r"Actor: (\w+)", content)
        for a in actors: stats["actors"][a] = stats["actors"].get(a, 0) + 1
        
        # Últimos Eventos
        matches = re.finditer(r"TRIGGERED: (.*?)\n.*?\nIP: (.*?) \| Actor: (.*?)\(", content)
        for m in list(matches)[-10:]:
            stats["recent_events"].append({"time": m.group(1), "ip": m.group(2).strip(), "actor": m.group(3).strip()})

    return stats

@app.route('/')
def index(): return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats(): return jsonify(parse_logs())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)
