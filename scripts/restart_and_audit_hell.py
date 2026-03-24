import paramiko
import sys
import json
import time

def restart_and_audit():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=20)
        
        results = {}

        # 1. Encender infraestructura
        print("--- INICIANDO CONTENEDORES ---")
        stdin, stdout, stderr = ssh.exec_command(f"cd {project_dir} && docker-compose up -d")
        results["docker_up"] = stdout.read().decode('utf-8') + stderr.read().decode('utf-8')
        
        # Esperar estabilización de red y bindeo de puertos
        time.sleep(5)

        # 2. Revisión de Contenedores
        stdin, stdout, stderr = ssh.exec_command("docker ps --format 'table {{.Names}}	{{.Status}}	{{.Ports}}'")
        results["container_status"] = stdout.read().decode('utf-8').strip()

        # 3. Verificación de Puertos (Trap & Void)
        # Buscamos el proceso de hell_core escuchando en el rango VOID o puertos críticos
        stdin, stdout, stderr = ssh.exec_command("netstat -tulnp | grep -E 'python|docker' | head -n 20")
        results["network_audit"] = stdout.read().decode('utf-8').strip()

        # 4. Verificación de Escritura de Logs
        stdin, stdout, stderr = ssh.exec_command(f"ls -lh {project_dir}/logs/ && tail -n 5 {project_dir}/logs/hell_core.log")
        results["log_audit"] = stdout.read().decode('utf-8').strip()

        # 5. Arsenal & Payloads Check
        stdin, stdout, stderr = ssh.exec_command(f"ls -R {project_dir}/assets/deception | head -n 20")
        results["arsenal_check"] = stdout.read().decode('utf-8').strip()

        # 6. Verificación de Bomba Fifield (SSH trap)
        stdin, stdout, stderr = ssh.exec_command("ls -lh /root/Active-Defense-Hell/assets/bombs/fifield_10G.bin || echo 'Bomba no encontrada'")
        results["bomb_check"] = stdout.read().decode('utf-8').strip()

        ssh.close()
        return results
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    report = restart_and_audit()
    print(json.dumps(report, indent=2))
