import os
import paramiko
import sys
import json

def forensic_elite_extraction():
    host = ""os.getenv('PRO_IP')""
    port = 2200
    user = "root"
    password = ""os.getenv('PRO_PASS')""
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=15)
        
        # Filtramos lucifer_mini.log para encontrar patrones de elite ports
        # y hell_activity.log para los flags de [ELITE_ENGAGEMENT]
        commands = {
            "recent_payloads": "grep -E 'PORT:(6443|8080|2375|2376|9200|5601|8081|5000|8000|11434)' /root/Active-Defense-Hell/logs/lucifer_mini.log | tail -n 20",
            "engagement_logs": "grep 'ELITE_ENGAGEMENT' /root/Active-Defense-Hell/logs/hell_activity.log | tail -n 20"
        }
        
        results = {}
        for key, cmd in commands.items():
            stdin, stdout, stderr = ssh.exec_command(cmd)
            results[key] = stdout.read().decode('utf-8').strip()
            
        ssh.close()
        return results
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    report = forensic_elite_extraction()
    print(json.dumps(report, indent=2))
