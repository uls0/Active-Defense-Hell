import os
import paramiko
import time

def inject_native_loot():
    host = ""os.getenv('PRO_IP')""
    port = 2200
    user = "root"
    password = ""os.getenv('PRO_PASS')""
    loot_file = "/root/Active-Defense-Hell/logs/credentials.log"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=15)
        
        ts = time.strftime('%H:%M:%S')
        test_loot = f"[{ts}] IP:127.0.0.1 | PORT:6379 | LOOT: root:NATIVE_POWER_2026"
        
        # Inyectar y asegurar permisos
        ssh.exec_command(f"echo '{test_loot}' >> {loot_file}")
        ssh.exec_command(f"chmod 666 {loot_file}")
        
        print(f"[✔] Loot nativo inyectado: {test_loot}")
        
        ssh.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    inject_native_loot()
