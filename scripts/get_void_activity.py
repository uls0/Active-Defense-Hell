import os
import paramiko

def get_void_logs():
    host = ""os.getenv('PRO_IP')""
    port = 2200
    user = "root"
    password = ""os.getenv('PRO_PASS')""
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=15)
        
        # Filtrar por el puerto 6666 que es el receptor del VOID
        stdin, stdout, stderr = ssh.exec_command("grep 'Port: 6666' /root/Active-Defense-Hell/logs/hell_activity.log | tail -n 20")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    get_void_logs()
