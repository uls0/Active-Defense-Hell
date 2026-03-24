import paramiko
import sys

def stop_hell_infrastructure():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=15)
        
        # 1. Detener vía docker-compose para apagado limpio
        # 2. Verificar que no queden contenedores huérfanos de HELL
        commands = [
            f"cd {project_dir} && docker-compose down",
            "docker ps -a --filter 'name=hell_' --format '{{.ID}}' | xargs -r docker stop",
            "docker ps --format 'table {{.Names}}	{{.Status}}'"
        ]
        
        print("--- INICIANDO PROTOCOLO DE APAGADO SEGURO ---")
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = stdout.read().decode('utf-8').strip()
            err = stderr.read().decode('utf-8').strip()
            if out: print(f"STDOUT: {out}")
            if err: print(f"STDERR: {err}")
            
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    stop_hell_infrastructure()
