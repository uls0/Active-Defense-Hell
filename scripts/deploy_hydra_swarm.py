import os
import paramiko

def deploy_hydra_mesh(host, peer):
    port = 2200 if host == ""os.getenv('PRO_IP')"" else 22
    user = "root"
    password = ""os.getenv('PRO_PASS')"" if host == ""os.getenv('PRO_IP')"" else ""os.getenv('SEC_PASS')""
    project_dir = "/root/Active-Defense-Hell"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=30)
        
        # Subir core Hydra
        sftp = ssh.open_sftp()
        sftp.put("C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/hell_core_hydra.py", f"{project_dir}/hell_core_hydra.py")
        sftp.close()
        
        # Actualizar servicio para usar core Hydra
        ssh.exec_command(f"sed -i 's/hell_core_native.py/hell_core_hydra.py/' /etc/systemd/system/hell.service")
        ssh.exec_command("systemctl daemon-reload && systemctl restart hell.service")
        
        print(f"--- NODO {host} ELEVADO A HYDRA MESH ---")
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR en {host}: {e}")
        return False

if __name__ == "__main__":
    deploy_hydra_mesh(""os.getenv('PRO_IP')"", ""os.getenv('SEC_IP')"")
    deploy_hydra_mesh(""os.getenv('SEC_IP')"", ""os.getenv('PRO_IP')"")
