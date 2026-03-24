import paramiko
import sys
import json

def forensic_incursion():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=10)
        
        commands = {
            "core_summary": "uptime && docker stats --no-stream --format 'table {{.Name}}	{{.CPUPerc}}	{{.MemUsage}}'",
            "critical_findings": "find /root/Active-Defense-Hell/malware -type f -mtime -1 | wc -l && tail -n 100 /root/Active-Defense-Hell/logs/hell_core.log | grep -iE 'critical|attack|malware' | tail -n 10",
            "cisco_trap": "docker logs hell_cisco 2>&1 | grep 'Login' | tail -n 5 || echo 'No active Cisco logins detected.'",
            "lucifer_report": "tail -n 50 /root/Active-Defense-Hell/logs/lucifer_mini.log 2>/dev/null || echo 'lucifer_mini.log not found. Checking alternate logs...' && tail -n 50 /root/Active-Defense-Hell/logs/lucifer.log 2>/dev/null"
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
    report = forensic_incursion()
    print(json.dumps(report, indent=2))
