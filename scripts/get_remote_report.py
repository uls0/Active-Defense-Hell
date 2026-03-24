import os
import paramiko
import sys

def get_report():
    host = ""os.getenv('PRO_IP')""
    port = 2200
    user = "root"
    password = ""os.getenv('PRO_PASS')""
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password)
        
        # Ejecutar comandos de telemetría y búsqueda de logs
        commands = [
            "echo '--- IPS EN ESPERA (REPORTE CONSOLIDADO) ---'",
            "docker logs hell_core 2>&1 | grep 'en espera' | sed 's/.*IP \\(.*\\) en espera.*/\\1/' | sort | uniq -c | sort -nr | head -n 30"
        ]
        
        full_output = ""
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            full_output += f"--- {cmd} ---\n{stdout.read().decode('utf-8')}\n"
            
        ssh.close()
        return full_output
    except Exception as e:
        return f"ERROR_CONEXION: {e}"

if __name__ == "__main__":
    print(get_report())
