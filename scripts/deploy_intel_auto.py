import paramiko
import os

def deploy_intel_auto():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    local_files = {
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/scripts/threat_intel_auto.py": f"{project_dir}/scripts/threat_intel_auto.py",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/scripts/hell-intel.service": "/etc/systemd/system/hell-intel.service"
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
        
        # Activar el nuevo servicio
        print("[!] Activando hell-intel.service...")
        ssh.exec_command("systemctl daemon-reload")
        ssh.exec_command("systemctl enable hell-intel.service")
        ssh.exec_command("systemctl restart hell-intel.service")
        
        print("--- INTELIGENCIA AUTOMÁTICA ACTIVADA ---")
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    deploy_intel_auto()
