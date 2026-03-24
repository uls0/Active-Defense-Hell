import paramiko
import json
import time

def comprehensive_audit():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=30)
        
        commands = {
            "system_resources": "uptime && free -h && df -h /",
            "process_integrity": "ps aux | grep -E 'hell_core|mariadb' | grep -v grep",
            "port_deployment": "netstat -tulnp | grep -E 'python3|mariadbd' | sort -n -k 4",
            "iptables_void": "iptables -t nat -L PREROUTING -n -v",
            "log_activity": "ls -lh /root/Active-Defense-Hell/logs/ && tail -n 5 /root/Active-Defense-Hell/logs/hell_activity.log",
            "docker_remnants": "dpkg -l | grep -i docker || echo 'No docker packages found.'",
            "service_status": "systemctl status hell.service --no-pager"
        }
        
        report = {}
        for key, cmd in commands.items():
            stdin, stdout, stderr = ssh.exec_command(cmd)
            report[key] = stdout.read().decode('utf-8').strip()
            
        ssh.close()
        return report
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    results = comprehensive_audit()
    print(json.dumps(results, indent=2))
