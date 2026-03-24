import paramiko
import os

def deploy_ransomware_trap():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    local_files = {
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/hell_core_native.py": f"{project_dir}/hell_core_native.py",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/scripts/generate_poison_vault.py": f"{project_dir}/scripts/generate_poison_vault.py"
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
        
        # 2. Generar el Vault
        print("[!] Generando Poison Vault en el VPS...")
        ssh.exec_command(f"python3 {project_dir}/scripts/generate_poison_vault.py")
        
        # 3. Reiniciar el servicio
        print("[!] Reiniciando hell.service...")
        ssh.exec_command("systemctl restart hell.service")
        
        print("--- TRAMPA RANSOMWARE ACTIVADA (v17.5) ---")
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    deploy_ransomware_trap()
