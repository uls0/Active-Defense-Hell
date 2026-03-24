import paramiko
import os

def deploy_native_hell():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    local_files = {
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/hell_core_native.py": f"{project_dir}/hell_core_native.py",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/scripts/hell.service": "/etc/systemd/system/hell.service"
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
        
        # 2. Configurar IPTABLES para el VOID
        print("[!] Configurando IPTABLES (20101-65535 -> 6666)...")
        ssh.exec_command("iptables -t nat -F") # Limpiar tablas NAT
        ssh.exec_command("iptables -t nat -A PREROUTING -p tcp --dport 20101:65535 -j REDIRECT --to-ports 6666")
        
        # 3. Activar el servicio Systemd
        print("[!] Activando hell.service...")
        ssh.exec_command("systemctl daemon-reload")
        ssh.exec_command("systemctl enable hell.service")
        ssh.exec_command("systemctl restart hell.service")
        
        print("--- HELL NATIVO v17.4 DESPLEGADO Y ACTIVADO ---")
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    deploy_native_hell()
