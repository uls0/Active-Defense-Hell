import paramiko
import os

def deploy_secondary_arsenal():
    host = "170.64.151.185"
    port = 22
    user = "root"
    password = "INK0uJ8j4a5xCR"
    project_dir = "/root/Active-Defense-Hell"
    
    local_files = {
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/hell_core_native.py": f"{project_dir}/hell_core_native.py",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/elite_deception.py": f"{project_dir}/elite_deception.py",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/templates/dashboard.html": f"{project_dir}/templates/dashboard.html",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/scripts/threat_intel_auto.py": f"{project_dir}/scripts/threat_intel_auto.py",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/scripts/hell.service": "/etc/systemd/system/hell.service",
        "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/scripts/hell-intel.service": "/etc/systemd/system/hell-intel.service",
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
        
        # 2. Generar Certificados SSL
        print("[!] Generando Certificados MexCapital...")
        ssh.exec_command(f"openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -subj '/C=MX/ST=CDMX/L=Ciudad de Mexico/O=MexCapital Servicios Financieros S.A. de C.V./OU=IT/CN=api-sec.mexcapital.com.mx' -keyout {project_dir}/assets/certs/mexcapital.key -out {project_dir}/assets/certs/mexcapital.crt")
        
        # 3. Generar Bomba Fifield
        print("[!] Generando Bomba Fifield (10GB)...")
        ssh.exec_command(f"dd if=/dev/zero bs=1M count=10240 | gzip -c > {project_dir}/assets/bombs/fifield_10G.bin.gz")
        
        # 4. Generar Poison Vault
        print("[!] Construyendo Poison Vault...")
        ssh.exec_command(f"python3 {project_dir}/scripts/generate_poison_vault.py")
        
        # 5. Configurar Red
        print("[!] Configurando Iptables para el VOID...")
        ssh.exec_command("iptables -t nat -A PREROUTING -p tcp --dport 20101:65535 -j REDIRECT --to-ports 6666")
        
        # 6. Activar Servicios
        print("[!] Activando Servicios HELL...")
        ssh.exec_command("systemctl daemon-reload && systemctl enable hell.service hell-intel.service && systemctl restart hell.service hell-intel.service")
        
        print("--- NODO SECUNDARIO HYDRA ONLINE ---")
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    deploy_secondary_arsenal()
