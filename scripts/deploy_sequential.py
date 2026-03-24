import paramiko
import os
import time

def deploy_sequential_host():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    local_files = {
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/hell_core.py": f"{project_dir}/hell_core.py",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/scripts/port_reaper.sh": f"{project_dir}/scripts/port_reaper.sh",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/docker-compose.yml": f"{project_dir}/docker-compose.yml"
    }
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=30)
        
        # 1. Subir archivos
        sftp = ssh.open_sftp()
        for local, remote in local_files.items():
            print(f"[i] Uploading: {remote}")
            sftp.put(local, remote)
        sftp.close()
        
        # 2. Ejecutar Reaper
        print("[!] Ejecutando Reaper y configurando Iptables...")
        ssh.exec_command(f"chmod +x {project_dir}/scripts/port_reaper.sh && {project_dir}/scripts/port_reaper.sh")
        time.sleep(5)
        
        # 3. Detener stack previo
        ssh.exec_command(f"cd {project_dir} && docker-compose down")
        
        # 4. Iniciar nuevo stack
        print("[!] Iniciando stack en Modo Host (Apertura Secuencial)...")
        ssh.exec_command(f"cd {project_dir} && docker-compose up -d --build")
        
        print("--- DESPLIEGUE INICIADO. MONITOREANDO LOGS... ---")
        
        # Esperar 10 segundos y ver los primeros puertos
        time.sleep(10)
        stdin, stdout, stderr = ssh.exec_command("docker logs hell_core --tail 20")
        print(stdout.read().decode())
        
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    deploy_sequential_host()
