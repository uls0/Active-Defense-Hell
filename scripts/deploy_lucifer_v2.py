import paramiko
import os

def deploy_lucifer_prime():
    nodes = {
        "PRO": ("178.128.72.149", 2200, "INK0uJ8j4a5xCn"),
        "SEC": ("170.64.151.185", 22, "INK0uJ8j4a5xCR")
    }
    
    project_dir = "/root/Active-Defense-Hell"
    
    for name, (host, port, pwd) in nodes.items():
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, "root", pwd, timeout=30)
            
            # 1. Subir archivos
            sftp = ssh.open_sftp()
            sftp.put("C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/scripts/lucifer_prime.py", f"{project_dir}/scripts/lucifer_prime.py")
            sftp.put("C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/scripts/lucifer-prime.service", "/etc/systemd/system/lucifer-prime.service")
            sftp.close()
            
            # 2. Modificar hell_core_hydra.py para que ignore el puerto 6666
            ssh.exec_command(f"sed -i 's/6666,//' {project_dir}/hell_core_hydra.py")
            
            # 3. Activar nuevo servicio
            print(f"[*] Nodo {name}: Activando Lucifer Prime...")
            ssh.exec_command("systemctl daemon-reload && systemctl enable lucifer-prime.service && systemctl restart lucifer-prime.service hell.service")
            
            ssh.close()
            print(f"[✔] Nodo {name} actualizado con Tarpit Avanzado.")
        except Exception as e:
            print(f"ERROR en {name}: {e}")

if __name__ == "__main__":
    deploy_lucifer_prime()
