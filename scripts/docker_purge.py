import paramiko

def docker_purge():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=30)
        
        commands = [
            "docker-compose -f /root/Active-Defense-Hell/docker-compose.yml down --rmi all --volumes --remove-orphans",
            "docker system prune -a --volumes -f",
            "apt-get remove -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
            "rm -rf /var/lib/docker",
            "rm -rf /etc/docker"
        ]
        
        print("--- INICIANDO PURGA TOTAL DE DOCKER ---")
        for cmd in commands:
            print(f"[!] Ejecutando: {cmd}")
            ssh.exec_command(cmd)
            
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    docker_purge()
