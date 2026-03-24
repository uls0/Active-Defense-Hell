import os
import paramiko
import sys
import json

def find_loot_logs():
    host = ""os.getenv('PRO_IP')""
    port = 2200
    user = "root"
    password = ""os.getenv('PRO_PASS')""
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=15)
        
        # 1. Buscamos archivos de logs de credenciales
        # 2. Leemos las ultimas 10 lineas para ver el formato (User:Pass)
        commands = {
            "file_search": "ls -R /root/Active-Defense-Hell/logs/ | grep -E 'cred|pass|auth|loot'",
            "peek_creds": "tail -n 10 /root/Active-Defense-Hell/logs/credentials.log 2>/dev/null || echo 'No credentials.log found.'",
            "peek_activity_creds": "grep -iE 'user|pass|login|auth' /root/Active-Defense-Hell/logs/hell_activity.log | tail -n 10"
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
    report = find_loot_logs()
    print(json.dumps(report, indent=2))
