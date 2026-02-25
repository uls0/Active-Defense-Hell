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
        "recent_events": [], "hits": 0
    }
    if not os.path.exists(LOG_FILE): return stats
    
    try:
        with open(LOG_FILE, "r", encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # Extraer daño total (Injected MB)
            data_matches = re.findall(r"Data: ([\d.]+)MB", content)
            stats["total_data"] = sum(float(d) for d in data_matches)
            
            # Extraer tiempo total (Retention seconds)
            time_matches = re.findall(r"Retention: ([\d.]+)s", content)
            stats["total_time"] = sum(float(t) for t in time_matches)
            
            # Contador de impactos
            stats["hits"] = len(re.findall(r"TRIGGERED:", content))
            
            # Perfiles de Actores
            actors = re.findall(r"Actor: (\w+)", content)
            for a in actors: stats["actors"][a] = stats["actors"].get(a, 0) + 1
            
            # Países
            origins = re.findall(r"Origin: (.*?),", content)
            for country in origins:
                stats["countries"][country] = stats["countries"].get(country, 0) + 1

            # Eventos Recientes (Últimos 10)
            matches = re.finditer(r"TRIGGERED: (.*?)\nIP: (.*?) \| Actor: (.*?)\(", content)
            for m in list(matches)[-10:]:
                stats["recent_events"].append({
                    "time": m.group(1),
                    "ip": m.group(2).strip(),
                    "actor": m.group(3).strip()
                })
    except: pass
    return stats

@app.route('/')
def index(): return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats(): return jsonify(parse_logs())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)
