import os
import paramiko
import json

def diagnose_mesh():
    nodes = {
        "PRO": (""os.getenv('PRO_IP')"", 2200, ""os.getenv('PRO_PASS')""),
        "SEC": (""os.getenv('SEC_IP')"", 22, ""os.getenv('SEC_PASS')"")
    }
    
    report = {}
    for name, (host, port, pwd) in nodes.items():
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, "root", pwd, timeout=10)
            
            stdin, stdout, stderr = ssh.exec_command("ps aux | grep hell_core_hydra.py | grep -v grep && netstat -tulnp | grep :8888")
            report[name] = stdout.read().decode('utf-8').strip() or "PROCESS_DEAD_OR_PORT_CLOSED"
            ssh.close()
        except Exception as e:
            report[name] = f"CONNECTION_ERROR: {e}"
            
    return report

if __name__ == "__main__":
    results = diagnose_mesh()
    print(json.dumps(results, indent=2))
