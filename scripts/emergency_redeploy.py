import paramiko
import os

def emergency_redeploy():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    local_files = {
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/hell_core.py": f"{project_dir}/hell_core.py",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/elite_deception.py": f"{project_dir}/elite_deception.py",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/scripts/dashboard_server.py": f"{project_dir}/scripts/dashboard_server.py",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/templates/dashboard.html": f"{project_dir}/templates/dashboard.html"
    }
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=30)
        
        # 1. Limpieza Agresiva
        print("[!] Matando procesos y contenedores...")
        ssh.exec_command("docker stop hell_core hell_db_backend && docker rm hell_core hell_db_backend")
        ssh.exec_command("fuser -k 8888/tcp 6666/tcp 22/tcp 6443/tcp 2375/tcp 2376/tcp 80/tcp 443/tcp")
        
        # 2. Subida de Archivos Golden
        sftp = ssh.open_sftp()
        for local, remote in local_files.items():
            print(f"[i] Uploading: {remote}")
            sftp.put(local, remote)
        sftp.close()
        
        # 3. Re-despliegue con Build Limpio
        print("[!] Iniciando stack...")
        ssh.exec_command(f"cd {project_dir} && docker-compose up -d --build")
        
        print("--- GOLDEN-CORE v17.1 MEXCAPITAL ONLINE ---")
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    emergency_redeploy()
