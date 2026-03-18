import paramiko
import os

def run_remote_incursion():
    host = '178.128.72.149'
    port = 2200
    user = 'root'
    password = 'INK0uJ8j4a5xCn'
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, port, user, password)
        sftp = ssh.open_sftp()
        sftp.put('LOGS/attacker_ips.txt', '/root/Active-Defense-Hell/logs/attacker_ips.txt')
        
        remote_script = """
import socket
import threading
import os

def poke_ip(ip):
    results = {"ip": ip, "ports": [], "ping": False}
    # Linux ping: -c 1 (1 count), -W 1 (1 sec timeout)
    response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
    if response == 0:
        results["ping"] = True
        
    for port in [22, 80, 443, 8080, 8443, 3389]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            res = s.connect_ex((ip, port))
            if res == 0:
                results["ports"].append(port)
            s.close()
        except: pass
        
    if results["ping"] or results["ports"]:
        line = "IP: " + str(ip) + " | Ping: " + str(results['ping']) + " | Ports: " + str(results['ports']) + "\\n"
        with open("/root/Active-Defense-Hell/logs/poke_results.log", "a") as f:
            f.write(line)

if __name__ == "__main__":
    if os.path.exists("/root/Active-Defense-Hell/logs/poke_results.log"):
        os.remove("/root/Active-Defense-Hell/logs/poke_results.log")
        
    with open("/root/Active-Defense-Hell/logs/attacker_ips.txt", "r") as f:
        ips = [line.strip() for line in f.readlines() if line.strip()]
    
    recent_ips = ips[-50:] # Los 50 más recientes
    print("[*] Incursion on " + str(len(recent_ips)) + " Lilin nodes started...")
    
    threads = []
    for ip in recent_ips:
        t = threading.Thread(target=poke_ip, args=(ip,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("[*] Incursion finished.")
"""
        with sftp.file('/root/Active-Defense-Hell/scripts/remote_poke_vps.py', 'w') as f:
            f.write(remote_script)
            
        sftp.close()
        
        print("[*] Lanzando contra-ataque de escaneo desde ADAM...")
        stdin, stdout, stderr = ssh.exec_command('python3 /root/Active-Defense-Hell/scripts/remote_poke_vps.py')
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        sftp = ssh.open_sftp()
        try:
            sftp.get('/root/Active-Defense-Hell/logs/poke_results.log', 'LOGS/poke_results_remote.log')
            print("[+] Resultados de la incursión descargados a LOGS/poke_results_remote.log")
        except:
            print("[!] No se generaron resultados (ningún Lilin respondió).")
        sftp.close()
        
    finally:
        ssh.close()

if __name__ == "__main__":
    run_remote_incursion()
