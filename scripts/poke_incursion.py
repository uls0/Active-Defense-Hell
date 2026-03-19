import socket, time, os, threading

TARGET_FILE = "/root/Active-Defense-Hell/logs/target_ips.txt"
LOG_OUT = "/root/Active-Defense-Hell/logs/poke_run.log"

def poke_ip(ip):
    # Intentar conexion a puertos comunes para disparar alertas en el atacante
    ports = [80, 443, 22, 3389]
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            s.close()
            with open(LOG_OUT, "a") as f:
                f.write(f"[OK] POKED: {ip}:{port} at {time.ctime()}\n")
        except: pass

def start_poking():
    if not os.path.exists(TARGET_FILE):
        print("[!] Target file not found.")
        return
    with open(TARGET_FILE, "r") as f:
        ips = f.read().splitlines()
    
    print(f"[*] Starting Re-Engagement for {len(ips)} targets...")
    for ip in ips:
        if ip.strip():
            threading.Thread(target=poke_ip, args=(ip.strip(),), daemon=True).start()
            time.sleep(0.2) # Delay para evitar baneo de ISP

if __name__ == "__main__":
    start_poking()
    # Mantener vivo un momento para que los hilos terminen
    time.sleep(30)
