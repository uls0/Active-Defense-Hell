import paramiko

host = "178.128.72.149"
port = 2200
user = "root"
password = "INK0uJ8j4a5xCn"

local_file = "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL/hell_core.py"
remote_file = "/root/Active-Defense-Hell/hell_core.py"

print("[*] Conectando al VPS HELL...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(host, port, user, password)
    
    print("[*] Subiendo hell_core.py actualizado...")
    sftp = ssh.open_sftp()
    sftp.put(local_file, remote_file)
    sftp.close()
    
    print("[*] Reiniciando contenedor hell_core...")
    stdin, stdout, stderr = ssh.exec_command("docker restart hell_core")
    print(f"[+] Salida: {stdout.read().decode('utf-8').strip()}")
    
    ssh.close()
    print("[+] Despliegue completado. HELL_CORE v13 actualizado con LUCIFER-Fifield-Bomb.")
except Exception as e:
    print(f"[!] Error durante el despliegue: {e}")
