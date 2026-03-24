import paramiko

def deploy_hydra_mesh(host, peer):
    port = 2200 if host == "178.128.72.149" else 22
    user = "root"
    password = "INK0uJ8j4a5xCn" if host == "178.128.72.149" else "INK0uJ8j4a5xCR"
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
    deploy_hydra_mesh("178.128.72.149", "170.64.151.185")
    deploy_hydra_mesh("170.64.151.185", "178.128.72.149")
