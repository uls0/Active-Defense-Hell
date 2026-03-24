import paramiko
import sys
import os

def restore_lethal_arsenal():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=30)
        
        # 1. Crear directorios base si no existen
        commands = [
            f"mkdir -p {project_dir}/assets/bombs",
            f"mkdir -p {project_dir}/assets/deception",
            f"mkdir -p {project_dir}/payloads",
            
            # 2. Generar la Bomba Fifield (Gzip Bomb) directamente en el VPS para evitar transferencia pesada
            # Usamos un comando dd + gzip para crearla rápido
            f"dd if=/dev/zero bs=1M count=10240 | gzip -c > {project_dir}/assets/bombs/fifield_10G.bin.gz",
            
            # 3. Generar archivos trampa de engaño (Honey-Files)
            f"echo 'CREDENTIAL_STUFFING_2026_DUMP' > {project_dir}/assets/deception/corporate_passwords.txt",
            f"head -c 1M </dev/urandom > {project_dir}/assets/deception/backup_db_20260324.sql.gz",
            f"echo 'VPN_CONFIG_INTERNAL' > {project_dir}/assets/deception/vpn_access.ovpn",
            
            # 4. Asegurar permisos para los contenedores
            f"chmod -R 777 {project_dir}/assets",
            f"chmod -R 777 {project_dir}/payloads",
            
            # 5. Reiniciar hell_core para que detecte el arsenal
            "docker restart hell_core"
        ]
        
        print("--- RECONSTRUYENDO ARSENAL LETHAL EN SENTINEL ---")
        for cmd in commands:
            print(f"[i] Ejecutando: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # Esperar a que dd/gzip terminen (puede tardar)
            stdout.channel.recv_exit_status()
            
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    restore_lethal_arsenal()
