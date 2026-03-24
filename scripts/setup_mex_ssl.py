import paramiko
import sys

def setup_mexcapital_identity():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    project_dir = "/root/Active-Defense-Hell"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=30)
        
        # Comandos para generar certificados SSL realistas
        commands = [
            f"mkdir -p {project_dir}/assets/certs",
            f"openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 "
            f"-subj '/C=MX/ST=CDMX/L=Ciudad de Mexico/O=MexCapital Servicios Financieros S.A. de C.V./OU=IT Infrastructure/CN=api-prod.mexcapital.com.mx' "
            f"-keyout {project_dir}/assets/certs/mexcapital.key -out {project_dir}/assets/certs/mexcapital.crt",
            f"chmod 644 {project_dir}/assets/certs/mexcapital.*"
        ]
        
        print("--- GENERANDO CERTIFICADOS SSL MEXCAPITAL ---")
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdout.channel.recv_exit_status()
            
        ssh.close()
        return True
    except Exception as e:
        print(f"ERROR SSL: {e}")
        return False

if __name__ == "__main__":
    setup_mexcapital_identity()
