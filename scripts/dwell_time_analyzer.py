import paramiko
from datetime import datetime
import json

def analyze_dwell_time():
    nodes = {
        "PRO": ("178.128.72.149", 2200, "INK0uJ8j4a5xCn"),
        "SEC": ("170.64.151.185", 22, "INK0uJ8j4a5xCR")
    }
    
    global_results = {}
    
    for name, (host, port, pwd) in nodes.items():
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, "root", pwd, timeout=15)
            
            # Leer las últimas 5000 líneas para tener una muestra estadística representativa
            stdin, stdout, stderr = ssh.exec_command("tail -n 5000 /root/Active-Defense-Hell/logs/hell_activity.log")
            lines = stdout.readlines()
            
            ip_sessions = {} # IP -> [first_ts, last_ts]
            
            for line in lines:
                try:
                    # Formato: [Hit] 2026-03-24 11:15:58 | IP: 1.2.3.4 | ...
                    parts = line.split("|")
                    ts_str = parts[0].split("]")[1].strip()
                    ts = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
                    ip = parts[1].replace("IP:", "").strip()
                    
                    if ip not in ip_sessions:
                        ip_sessions[ip] = [ts, ts]
                    else:
                        ip_sessions[ip][1] = ts
                except: continue
            
            durations = []
            for ip, (start, end) in ip_sessions.items():
                diff = (end - start).total_seconds()
                if diff > 0: # Ignorar hits únicos para el promedio de permanencia
                    durations.append(diff)
            
            avg_time = sum(durations) / len(durations) if durations else 0
            max_time = max(durations) if durations else 0
            
            global_results[name] = {
                "avg_dwell_seconds": round(avg_time, 2),
                "max_dwell_seconds": round(max_time, 2),
                "total_active_bots": len(ip_sessions),
                "recurring_bots": len(durations)
            }
            ssh.close()
        except Exception as e:
            global_results[name] = {"error": str(e)}
            
    return global_results

if __name__ == "__main__":
    results = analyze_dwell_time()
    print(json.dumps(results, indent=2))
