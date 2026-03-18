import paramiko

def get_sachiel_targets():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    
    # Comando limpio para extraer IPs de SACHIEL
    cmd = "grep -B 5 'SACHIEL-RDP-ENGAGEMENT' /root/Active-Defense-Hell/logs/hell_activity.log | grep 'IP:' | awk '{print $2}' | sort | uniq"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("--- LILIN CAPTURADOS EN SACHIEL (RDP) ---")
        print(stdout.read().decode('utf-8'))
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_sachiel_targets()
