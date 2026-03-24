import paramiko
from datetime import datetime
import json

def analyze_hydra_performance():
    nodes = {
        "PRO": ("178.128.72.149", 2200, "INK0uJ8j4a5xCn"),
        "SEC": ("170.64.151.185", 22, "INK0uJ8j4a5xCR")
    }
    
    global_report = {}
    
    for name, (host, port, pwd) in nodes.items():
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, "root", pwd, timeout=15)
            
            # Analizar Hell Activity (Mesh/Elite) y Lucifer Prime (Tarpit)
            commands = {
                "hell_logs": "tail -n 3000 /root/Active-Defense-Hell/logs/hell_activity.log",
                "lucifer_logs": "tail -n 1000 /root/Active-Defense-Hell/logs/lucifer_prime.log 2>/dev/null || echo ''"
            }
            
            ip_data = {} # IP -> {first, last, hits, types: []}
            mirror_hits = 0
            bomb_triggers = 0
            
            for key, cmd in commands.items():
                stdin, stdout, stderr = ssh.exec_command(cmd)
                lines = stdout.readlines()
                
                for line in lines:
                    try:
                        if "|" in line:
                            # Formato Hell Activity
                            parts = line.split("|")
                            ts_str = parts[0].split("]")[1].strip()
                            ts = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
                            ip = parts[1].replace("IP:", "").strip()
                            
                            if "MIRRORING" in line: mirror_hits += 1
                            
                            if ip not in ip_data:
                                ip_data[ip] = {"first": ts, "last": ts, "hits": 1}
                            else:
                                ip_data[ip]["last"] = ts
                                ip_data[ip]["hits"] += 1
                        
                        elif "VOID_ENTRY" in line:
                            # Formato Lucifer Prime
                            parts = line.split("]")
                            ts_str = parts[0].replace("[", "").strip()
                            ts = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
                            ip = line.split("VOID_ENTRY:")[1].split("|")[0].strip()
                            
                            if "BOMB_DEPLOYED" in line: bomb_triggers += 1
                            
                            if ip not in ip_data:
                                ip_data[ip] = {"first": ts, "last": ts, "hits": 1}
                            else:
                                ip_data[ip]["last"] = ts
                                ip_data[ip]["hits"] += 1
                    except: continue

            durations = [(d["last"] - d["first"]).total_seconds() for d in ip_data.values() if (d["last"] - d["first"]).total_seconds() > 0]
            
            global_report[name] = {
                "avg_dwell_time": f"{sum(durations)/len(durations):.2f}s" if durations else "0s",
                "max_dwell_time": f"{max(durations):.2f}s" if durations else "0s",
                "mirroring_events": mirror_hits,
                "fifield_bombs_injected": bomb_triggers,
                "unique_attackers": len(ip_data)
            }
            ssh.close()
        except Exception as e:
            global_report[name] = {"error": str(e)}
            
    return global_report

if __name__ == "__main__":
    report = analyze_hydra_performance()
    print(json.dumps(report, indent=2))
