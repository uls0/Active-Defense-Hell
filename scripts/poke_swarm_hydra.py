import paramiko
import os

def execute_poke_swarm():
    nodes = {
        "PRO": (""os.getenv('PRO_IP')"", 2200, ""os.getenv('PRO_PASS')""),
        "SEC": (""os.getenv('SEC_IP')"", 22, ""os.getenv('SEC_PASS')"")
    }
    
    project_dir = "/root/Active-Defense-Hell"
    
    for name, (host, port, pwd) in nodes.items():
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, "root", pwd, timeout=15)
            
            # 1. Extraer IPs de los logs para crear target_ips.txt dinámicamente
            print(f"[*] Nodo {name}: Extrayendo objetivos agresivos...")
            extract_cmd = f"grep 'Port:' {project_dir}/logs/hell_activity.log | awk -F'IP:' '{{print $2}}' | awk -F'|' '{{print $1}}' | sort | uniq | tail -n 50 > {project_dir}/logs/target_ips.txt"
            ssh.exec_command(extract_cmd)
            
            # 2. Ejecutar Poke-Incursion en segundo plano
            print(f"[!] Nodo {name}: Lanzando SWARM RE-ENGAGEMENT...")
            ssh.exec_command(f"nohup python3 {project_dir}/scripts/poke_incursion.py > {project_dir}/logs/poke_results_hydra.log 2>&1 &")
            
            ssh.close()
        except Exception as e:
            print(f"ERROR en {name}: {e}")

if __name__ == "__main__":
    execute_poke_swarm()
