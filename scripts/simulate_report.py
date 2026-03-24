import os
import paramiko
import time

def simulate_elite_attack():
    host = ""os.getenv('PRO_IP')""
    port = 2200
    user = "root"
    password = ""os.getenv('PRO_PASS')""
    log_file = "/root/Active-Defense-Hell/logs/hell_activity.log"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=15)
        
        # Simular un hit en puerto Elite (K8s)
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        # Formato: [Hit] 2026-03-24 11:15:58 | IP: 9.9.9.9 | Port: 6443 | State: ENGAGED | Info: 
        attack_log = f"[Hit] {ts} | IP: 9.9.9.9 | Port: 6443 | State: ENGAGED | Info: MEXCAPITAL_TEST_REPORT"
        
        print(f"[*] Inyectando ataque simulado: {attack_log}")
        ssh.exec_command(f"echo '{attack_log}' >> {log_file}")
        
        # Dar tiempo al servicio de inteligencia para procesar
        time.sleep(5)
        
        print("[*] Revisando logs del servicio de inteligencia (hell-intel.service)...")
        stdin, stdout, stderr = ssh.exec_command("journalctl -u hell-intel.service -n 10 --no-pager")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    simulate_elite_attack()
