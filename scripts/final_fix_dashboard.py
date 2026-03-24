import os
import paramiko
import time

def final_fix_loot_dashboard():
    host = ""os.getenv('PRO_IP')""
    port = 2200
    user = "root"
    password = ""os.getenv('PRO_PASS')""
    project_dir = "/root/Active-Defense-Hell"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=30)
        
        # 1. Matar cualquier proceso en el puerto 8888 y detener contenedor
        print("[!] Limpiando puerto 8888...")
        ssh.exec_command("docker stop hell_core")
        ssh.exec_command("fuser -k 8888/tcp")
        time.sleep(2)
        
        # 2. Subir los archivos corregidos (estamos asumiendo que ya los edité localmente)
        sftp = ssh.open_sftp()
        sftp.put("C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/scripts/dashboard_server.py", 
                 f"{project_dir}/scripts/dashboard_server.py")
        sftp.put("C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/templates/dashboard.html", 
                 f"{project_dir}/templates/dashboard.html")
        sftp.put("C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/hell_core.py", 
                 f"{project_dir}/hell_core.py")
        sftp.put("C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/elite_deception.py", 
                 f"{project_dir}/elite_deception.py")
        sftp.close()
        
        # 3. Asegurar permisos de logs
        ssh.exec_command(f"touch {project_dir}/logs/credentials.log && chmod 666 {project_dir}/logs/credentials.log")
        
        # 4. Iniciar el stack de nuevo
        print("[!] Reiniciando infraestructura...")
        ssh.exec_command(f"cd {project_dir} && docker-compose up -d --build")
        
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    final_fix_loot_dashboard()
