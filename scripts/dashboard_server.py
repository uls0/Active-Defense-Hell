from flask import Flask, render_template, jsonify
import json
import os
import re
import subprocess
import sys

app = Flask(__name__, template_folder='../templates')
LOG_FILE = "logs/hell_activity.log"

def get_kernel_blocks():
    try:
        result = subprocess.run(["iptables", "-L", "INPUT", "-n"], capture_output=True, text=True, timeout=2)
        return list(set(re.findall(r"DROP\s+all\s+--\s+([\d\.]+)", result.stdout)))
    except: return []

@app.route('/api/stats')
def get_stats():
    stats = {"total_data": 0, "total_time": 0, "actors": {}, "recent_events": [], "kernel_blocks": get_kernel_blocks()}
    if not os.path.exists(LOG_FILE): return jsonify(stats)
    
    try:
        with open(LOG_FILE, "r", encoding='utf-8', errors='ignore') as f:
            content = f.read()
            stats["total_data"] = sum(float(d) for d in re.findall(r"Injected: ([\d.]+)MB", content))
            stats["total_time"] = sum(float(t) for t in re.findall(r"Retention: ([\d.]+)s", content))
            actors = re.findall(r"Actor: (\w+)", content)
            for a in actors: stats["actors"][a] = stats["actors"].get(a, 0) + 1
            matches = re.finditer(r"TRIGGERED: (.*?)\n.*?\nIP: (.*?) \| Actor: (.*?)\(", content)
            for m in list(matches)[-10:]:
                stats["recent_events"].append({"time": m.group(1), "ip": m.group(2).strip(), "actor": m.group(3).strip()})
    except: pass
    return jsonify(stats)

@app.route('/')
def index(): return render_template('dashboard.html')

if __name__ == "__main__":
    # Intentar puertos del 8888 al 8898 para evitar bloqueos
    port = 8888
    success = False
    while port < 8900 and not success:
        try:
            print(f"[*] Dashboard attempting to start on port {port}...")
            app.run(host='0.0.0.0', port=port)
            success = True
        except Exception as e:
            print(f"[!] Port {port} occupied, trying next...")
            port += 1
    if not success: sys.exit(1)
