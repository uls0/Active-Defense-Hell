import paramiko
import sys
import os

def patch_and_deploy_core():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=30)
        
        # 1. Subir elite_deception.py
        sftp = ssh.open_sftp()
        local_elite = "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/elite_deception.py"
        sftp.put(local_elite, f"{project_dir}/elite_deception.py")
        
        # 2. Modificar hell_core.py
        # Usaremos sed y echo para parches más seguros que eviten errores de escape
        patch_commands = [
            f"sed -i '1i from elite_deception import EliteHandler' {project_dir}/hell_core.py",
            f"sed -i '/os.makedirs(\"payloads\", exist_ok=True)/a \\        self.elite = EliteHandler(self.log_event)' {project_dir}/hell_core.py",
            # Inyectar logica elite_ports antes de ramiel_tarpit
            f"sed -i '/ramiel_tarpit.handle_drip/i \\        elite_ports = [6443, 8080, 2375, 2376, 9100, 9090, 9200, 5601, 6379, 11211, 8081, 3000, 5000, 8000, 11434]\\n        if local_port in elite_ports:\\n            self.elite.dispatch(client_socket, addr, local_port)\\n            return' {project_dir}/hell_core.py"
        ]
        
        for cmd in patch_commands:
            ssh.exec_command(cmd)
            
        # 3. Reiniciar
        ssh.exec_command(f"cd {project_dir} && docker-compose up -d --build")
        
        print("--- SISTEMA MEXCAPITAL-FINANCIAL DESPLEGADO CON ÉXITO ---")
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    patch_and_deploy_core()
