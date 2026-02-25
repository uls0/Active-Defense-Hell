from flask import Flask, render_template, jsonify
import json
import os
import re

app = Flask(__name__)
LOG_FILE = "logs/hell_activity.log"
MESH_INTEL = "logs/mesh_intel.json"

def parse_logs():
    """Parsea el log para extraer estadísticas de ataque"""
    stats = {"total_time": 0, "total_data": 0, "attacks": [], "countries": {}, "ports": {}}
    if not os.path.exists(LOG_FILE): return stats
    
    with open(LOG_FILE, "r", encoding='utf-8') as f:
        content = f.read()
        
        # Extraer daños totales
        times = re.findall(r"Time Lost: ([\d.]+)s", content)
        data = re.findall(r"Data Injected: ([\d.]+)MB", content)
        stats["total_time"] = sum(float(t) for t in times)
        stats["total_data"] = sum(float(d) for d in data)
        
        # Extraer países (basado en el formato de log ULTIMATE)
        origins = re.findall(r"Origin: (.*?) \|", content)
        for loc in origins:
            country = loc.split(",")[-1].strip()
            stats["countries"][country] = stats["countries"].get(country, 0) + 1
            
        # Extraer Puertos
        target_ports = re.findall(r"Target Port: (\d+)", content)
        for port in target_ports:
            stats["ports"][port] = stats["ports"].get(port, 0) + 1

    return stats

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    return jsonify(parse_logs())

@app.route('/api/mesh')
def get_mesh():
    if os.path.exists(MESH_INTEL):
        with open(MESH_INTEL, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({"blacklist": {}})

if __name__ == "__main__":
    # El dashboard corre en el puerto 8888
    app.run(host='0.0.0.0', port=8888)
