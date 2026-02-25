from flask import Flask, render_template, jsonify
import json
import os
import re

app = Flask(__name__, template_folder='../templates')
LOG_FILE = "logs/hell_activity.log"

def parse_logs():
    stats = {
        "total_time": 0, "total_data": 0, 
        "countries": {}, "ports": {}, 
        "actors": {}, "tools": {},
        "recent_events": []
    }
    if not os.path.exists(LOG_FILE): return stats
    
    with open(LOG_FILE, "r", encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
        # Totales
        stats["total_time"] = sum(float(t) for t in re.findall(r"Time Lost: ([\d.]+)s", content))
        stats["total_data"] = sum(float(d) for d in re.findall(r"Injected: ([\d.]+)MB", content))
        
        # Perfiles de Actores
        actors = re.findall(r"Actor: (\w+)", content)
        for a in actors: stats["actors"][a] = stats["actors"].get(a, 0) + 1
        
        # Herramientas (JA3)
        tools = re.findall(r"JA3: (\w+)", content)
        for t in tools: stats["tools"][t] = stats["tools"].get(t, 0) + 1

        # Orígenes
        origins = re.findall(r"Origin: (.*?) \|", content)
        for loc in origins:
            country = loc.split(",")[-1].strip()
            stats["countries"][country] = stats["countries"].get(country, 0) + 1

        # Eventos Recientes (Últimos 5)
        matches = re.finditer(r"TRIGGERED: (.*?)\n.*?\nIP: (.*?) \| Actor: (.*?)\(", content)
        for m in list(matches)[-5:]:
            stats["recent_events"].append({
                "time": m.group(1),
                "ip": m.group(2).strip(),
                "actor": m.group(3).strip()
            })

    return stats

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    return jsonify(parse_logs())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)
