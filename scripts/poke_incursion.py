import socket
import threading
import os

def poke_ip(ip):
    results = {"ip": ip, "ports": [], "ping": False}
    
    # 1. Ping
    response = os.system(f"ping -n 1 -w 500 {ip} > nul")
    if response == 0:
        results["ping"] = True
        
    # 2. Port Check
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
        print(f"[!] LILIN {ip} RESPONDED: Ping={results['ping']} | Ports={results['ports']}")
        with open("LOGS/poke_results.log", "a", encoding='utf-8') as f:
            f.write(f"IP: {ip} | Ping: {results['ping']} | Ports: {results['ports']}
")

def main():
    if not os.path.exists("LOGS/attacker_ips.txt"):
        print("Error: No IPs found.")
        return
        
    with open("LOGS/attacker_ips.txt", "r") as f:
        ips = [line.strip() for line in f.readlines() if line.strip()]
    
    # Tomar las últimas 50 IPs capturadas (las más recientes)
    recent_ips = ips[-50:]
    print(f"[*] INICIANDO INCURSIÓN: Picando a {len(recent_ips)} Lilin...")
    
    threads = []
    for ip in recent_ips:
        t = threading.Thread(target=poke_ip, args=(ip,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("[*] INCURSIÓN COMPLETADA. REVISAR LOGS/poke_results.log")

if __name__ == "__main__":
    main()
