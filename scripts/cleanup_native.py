import paramiko

def script_and_package_cleanup():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=30)
        
        # 1. Purgar paquetes de Docker restantes
        print("[!] Eliminando paquetes de Docker...")
        ssh.exec_command("apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker.io docker-compose")
        ssh.exec_command("apt-get autoremove -y && apt-get autoclean")
        
        # 2. Corregir scripts que usen Docker
        # Buscamos archivos que contengan la palabra 'docker'
        stdin, stdout, stderr = ssh.exec_command(f"grep -l 'docker' {project_dir}/scripts/*.py")
        files_to_fix = stdout.read().decode('utf-8').splitlines()
        
        print(f"[i] Scripts detectados con referencias a Docker: {files_to_fix}")
        
        # 3. Eliminar archivos de Docker obsoletos en el directorio
        ssh.exec_command(f"rm -f {project_dir}/Dockerfile {project_dir}/docker-compose.yml {project_dir}/entrypoint.sh")
        
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    script_and_package_cleanup()
