import paramiko

def check_sachiel_hits():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    
    cmd = "grep 'SACHIEL-RDP-ENGAGEMENT' /root/Active-Defense-Hell/logs/hell_activity.log | tail -n 20"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        results = stdout.read().decode('utf-8')
        if results:
            print("--- IMPACTOS EN SACHIEL (RDP WIN7) ---")
            print(results)
        else:
            print("[!] Sin impactos detectados en SACHIEL hasta el momento.")
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_sachiel_hits()
