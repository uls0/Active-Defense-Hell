import socket, time, os, threading

TARGET_FILE = "/root/Active-Defense-Hell/logs/target_ips.txt"
XP_NODES = ["33893", "33894"]

def poke_ip(ip):
    # Intentar conexion a puertos comunes para disparar alertas en el atacante
    for port in [80, 443, 22, 3389]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            s.close()
            print(f"[*] POKED: {ip}:{port}")
        except: pass

def start_poking():
    if not os.path.exists(TARGET_FILE): return
    with open(TARGET_FILE, "r") as f:
        ips = f.read().splitlines()
    
    print(f"[*] Starting Re-Engagement for {len(ips)} targets...")
    for ip in ips:
        threading.Thread(target=poke_ip, args=(ip,), daemon=True).start()
        time.sleep(0.1)

def simulate_xp_beacon():
    # Simular trafico NetBIOS/DHCP/AD para atraer bots
    print("[*] Starting Windows XP Beaconing Sim...")
    while True:
        for port in XP_NODES:
            # Emitir ruido tecnico simulado
            print(f"[BEACON] Node {port} announcing presence to GRID...")
            time.sleep(30)

if __name__ == "__main__":
    threading.Thread(target=simulate_xp_beacon, daemon=True).start()
    start_poking()
    while True: time.sleep(1)
