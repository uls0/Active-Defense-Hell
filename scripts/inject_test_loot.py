import paramiko
import time

def inject_test_loot():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=15)
        
        ts = time.strftime('%H:%M:%S')
        test_loot = f"[{ts}] IP:1.2.3.4 | PORT:6379 | LOOT: admin:MEXCAPITAL_PASS_TEST_2026"
        
        # Inyección directa en el log de credentials
        ssh.exec_command(f"echo '{test_loot}' >> /root/Active-Defense-Hell/logs/credentials.log")
        print(f"[✔] Credencial inyectada: {test_loot}")
        
        ssh.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    inject_test_loot()
