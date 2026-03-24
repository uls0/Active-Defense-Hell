import paramiko
import time

def stability_check():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=15)
        
        # Verificamos contenedores y logs del proceso de bindeo
        stdin, stdout, stderr = ssh.exec_command("docker ps --format '{{.Names}}: {{.Status}}' && docker logs hell_core --tail 15")
        print("--- STATUS REBALANCING ---")
        print(stdout.read().decode())
        
        # Verificamos si los puertos Gold ya empezaron a abrirse
        stdin, stdout, stderr = ssh.exec_command("netstat -tulnp | grep -E 'python|docker' | wc -l")
        print(f"Puertos bindeados actualmente: {stdout.read().decode().strip()}")
        
        ssh.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    stability_check()
