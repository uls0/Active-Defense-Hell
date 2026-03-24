import os
import paramiko

def setup_native_infra():
    host = ""os.getenv('PRO_IP')""
    port = 2200
    user = "root"
    password = ""os.getenv('PRO_PASS')""
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=60)
        
        # Usamos comillas simples para envolver el comando mariadb
        commands = [
            "apt-get update",
            "apt-get install -y python3-pip python3-dev mariadb-server libmariadb-dev-compat psmisc net-tools iptables",
            "systemctl start mariadb && systemctl enable mariadb",
            "mariadb -e 'CREATE DATABASE IF NOT EXISTS hell_forensics;'",
            "mariadb -e \"CREATE USER IF NOT EXISTS 'hell_user'@'localhost' IDENTIFIED BY '"os.getenv('DB_PASS')"';\"",
            "mariadb -e \"GRANT ALL PRIVILEGES ON hell_forensics.* TO 'hell_user'@'localhost';\"",
            "mariadb -e 'FLUSH PRIVILEGES;'",
            "pip3 install mysql-connector-python requests paramiko psutil --break-system-packages"
        ]
        
        print("--- INSTALANDO DEPENDENCIAS NATIVAS ---")
        for cmd in commands:
            print(f"[i] Ejecutando: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout.channel.recv_exit_status()
            
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    setup_native_infra()
