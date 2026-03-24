import paramiko
import sys

def update_ports_on_vps():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    ports_to_add = [
        "6443:6443", "8080:8080", "2375:2375", "2376:2376",
        "9100:9100", "9090:9090", "9200:9200", "5601:5601",
        "6379:6379", "11211:11211", "8081:8081", "3000:3000",
        "5000:5000", "8000:8000", "11434:11434"
    ]
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=30)
        
        # 1. Leer docker-compose actual
        stdin, stdout, stderr = ssh.exec_command(f"cat {project_dir}/docker-compose.yml")
        content = stdout.read().decode('utf-8')
        
        # 2. Inyectar puertos si no existen
        for p in ports_to_add:
            if p not in content:
                # Inyectar después de la cabecera 'ports:' del contenedor hell_core
                content = content.replace("    ports:", f"    ports:\n      - \"{p}\"")
            
        # 3. Escribir de vuelta el archivo
        sftp = ssh.open_sftp()
        with sftp.file(f"{project_dir}/docker-compose.yml", 'w') as f:
            f.write(content)
        sftp.close()
        
        print("--- DOCKER-COMPOSE ACTUALIZADO CON PUERTOS ELITE ---")
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    update_ports_on_vps()
