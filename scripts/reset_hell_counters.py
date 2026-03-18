import paramiko
import sys

def reset_counters():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password)
        
        # Ejecutar comandos de limpieza y reinicio de contadores
        commands = [
            "echo '[*] REINICIANDO CONTADORES DIARIOS (docker restart)...'",
            "docker restart hell_core",
            "echo '[*] PURGANDO ARCHIVOS DE EVIDENCIA ANTIGUOS...'",
            "rm -rf /root/Active-Defense-Hell/logs/forensics/*",
            "rm -rf /root/Active-Defense-Hell/logs/malware/*",
            "rm -rf /root/Active-Defense-Hell/logs/abuse_reports/*",
            "echo '[+] SISTEMA DE REPORTES REHABILITADO.'",
            "docker ps | grep hell_core"
        ]
        
        full_output = ""
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            full_output += stdout.read().decode('utf-8') + "\n"
            
        ssh.close()
        return full_output
    except Exception as e:
        return f"ERROR_CONEXION: {e}"

if __name__ == "__main__":
    print(reset_counters())
