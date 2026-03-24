import paramiko
import json

def diagnose_and_rollback():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=20)
        
        # 1. Diagnóstico de Docker
        commands = {
            "docker_status": "docker ps -a --format 'table {{.Names}}	{{.Status}}	{{.Ports}}'",
            "docker_errors": "docker logs hell_core --tail 20",
            "port_check": "netstat -tulnp | grep -E 'python|docker'",
            "disk_space": "df -h /"
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
    report = diagnose_and_rollback()
    print(json.dumps(report, indent=2))
