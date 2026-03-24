import paramiko
import os

def deploy_loot_module():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    local_files = {
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/elite_deception.py": f"{project_dir}/elite_deception.py",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/scripts/dashboard_server.py": f"{project_dir}/scripts/dashboard_server.py",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/templates/dashboard.html": f"{project_dir}/templates/dashboard.html"
    }
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=30)
        sftp = ssh.open_sftp()
        
        for local, remote in local_files.items():
            print(f"[i] Uploading: {remote}")
            sftp.put(local, remote)
            
        sftp.close()
        
        # Crear el archivo de logs si no existe para evitar errores
        ssh.exec_command(f"touch {project_dir}/logs/credentials.log && chmod 666 {project_dir}/logs/credentials.log")
        
        # Reiniciar stack
        ssh.exec_command(f"cd {project_dir} && docker-compose up -d --build")
        
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    deploy_loot_module()
