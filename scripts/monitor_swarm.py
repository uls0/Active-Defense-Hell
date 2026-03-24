import os
import paramiko
import json
import time

def monitor_swarm_return():
    nodes = {
        "PRO": (""os.getenv('PRO_IP')"", 2200, ""os.getenv('PRO_PASS')""),
        "SEC": (""os.getenv('SEC_IP')"", 22, ""os.getenv('SEC_PASS')"")
    }
    
    results = {}
    for name, (host, port, pwd) in nodes.items():
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, "root", pwd, timeout=10)
            
            # Contar hits en los últimos 2 minutos
            # Usamos un comando que busque hits recientes
            stdin, stdout, stderr = ssh.exec_command("tail -n 100 /root/Active-Defense-Hell/logs/hell_activity.log | wc -l")
            hits_count = stdout.read().decode('utf-8').strip()
            
            # Ver IPs que están regresando
            stdin, stdout, stderr = ssh.exec_command("tail -n 10 /root/Active-Defense-Hell/logs/hell_activity.log")
            recent_activity = stdout.read().decode('utf-8').strip()
            
            results[name] = {
                "hits_last_cycle": hits_count,
                "recent_activity": recent_activity
            }
            ssh.close()
        except:
            results[name] = "NODE_UNREACHABLE"
            
    return results

if __name__ == "__main__":
    time.sleep(10) # Esperar a que el swarm genere ruido
    report = monitor_swarm_return()
    print(json.dumps(report, indent=2))
