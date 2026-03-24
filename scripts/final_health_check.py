import os
import paramiko

def native_health_check():
    host = ""os.getenv('PRO_IP')""
    port = 2200
    user = "root"
    password = ""os.getenv('PRO_PASS')""
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=15)
        
        # 1. Verificar si el proceso de python está vivo
        # 2. Contar puertos bindeados por python
        # 3. Ver logs recientes de systemd
        commands = [
            "ps aux | grep hell_core_native.py | grep -v grep",
            "netstat -tulnp | grep python3 | wc -l",
            "journalctl -u hell.service -n 10"
        ]
        
        print("--- NATIVE HEALTH CHECK ---")
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(f"[i] Output of {cmd}:")
            print(stdout.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    native_health_check()
