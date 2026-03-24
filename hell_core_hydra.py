import os, threading, time, socket, sys, json, random, ssl
import requests

# =============================================================================
# HELL CORE v17.6.1 - HYDRA STABLE (MEXCAPITAL)
# =============================================================================

VERSION = "v17.6.1-HYDRA"
BASE_DIR = "/root/Active-Defense-Hell"
LOG_DIR = f"{BASE_DIR}/logs"
LOG_FILE = f"{LOG_DIR}/hell_activity.log"
LOOT_FILE = f"{LOG_DIR}/credentials.log"
HOST = '0.0.0.0'

# Puertos a patrullar
ALL_PORTS = [21, 22, 23, 25, 53, 80, 81, 88, 110, 111, 135, 137, 139, 143, 161, 179, 389, 443, 445, 502, 1433, 3306, 3389, 6443, 8080, 2375, 2376, 9100, 9090, 9200, 5601, 6379, 11211, 8081, 3000, 5000, 8000, 11434, 6666, 2049, 873]

# Auto-deteccion de IPs para el Mesh
try:
    MY_IP = requests.get('https://api.ipify.org', timeout=5).text
except:
    MY_IP = "UNKNOWN"
PEER_IP = ""os.getenv('SEC_IP')"" if MY_IP == ""os.getenv('PRO_IP')"" else ""os.getenv('PRO_IP')""

def log_event(ip, port, action="Hit", status="ENGAGED", info=""):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    report = f"[{action}] {ts} | IP: {ip} | Port: {port} | State: {status} | Info: {info}\n"
    if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(report); f.flush(); os.fsync(f.fileno())

def start_dashboard():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, 8888))
        server.listen(100)
        while True:
            client, addr = server.accept()
            try:
                raw = client.recv(4096).decode('utf-8', errors='ignore')
                first_line = raw.split('\n')[0] if '\n' in raw else raw
                
                if "/api/stats" in first_line:
                    hits = 0; events = []
                    if os.path.exists(LOG_FILE):
                        with open(LOG_FILE, "r") as f:
                            lines = f.readlines(); hits = len(lines)
                            for l in lines[-15:]:
                                try:
                                    p = l.split("|")
                                    events.append({"time": p[0].strip(), "ip": p[1].replace("IP:","").strip(), "port": p[2].replace("Port:","").strip(), "network": "HYDRA_MESH", "tactic": p[3].replace("State:","").strip()})
                                except: pass
                    
                    # Unificación Mesh con Timeout ULTRA agresivo (0.1s)
                    peer_hits = 0
                    try:
                        r = requests.get(f"http://{PEER_IP}:8888/api/stats", timeout=0.1)
                        if r.status_code == 200:
                            peer_hits = r.json().get("hits", 0)
                            events.extend(r.json().get("recent_events", []))
                    except: pass

                    res = json.dumps({"hits": hits + peer_hits, "total_data": (hits + peer_hits)*0.18, "recent_events": events[-20:], "botnets": [], "countries": {"MESH_ACTIVE": hits + peer_hits}})
                    client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(res)}\r\n\r\n{res}".encode())
                
                elif "/api/loot" in first_line:
                    loot = []
                    if os.path.exists(LOOT_FILE):
                        with open(LOOT_FILE, "r") as f: loot = [l.strip() for l in f.readlines()[-10:]]
                    res = json.dumps({"loot": loot})
                    client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(res)}\r\n\r\n{res}".encode())
                
                else:
                    template_path = f"{BASE_DIR}/templates/dashboard.html"
                    content = "<h1>HELL MESH DASHBOARD</h1>"
                    if os.path.exists(template_path):
                        with open(template_path, "r") as f: content = f.read()
                    client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content.encode('utf-8'))}\r\n\r\n{content}".encode())
            except: pass
            finally: client.close()
    except Exception as e: print(f"[!] Dashboard Fatal: {e}")

def handle_client(client_socket, addr, local_port):
    ip = addr[0]
    try:
        # Mirroring (20% Prob)
        if local_port in [6443, 2376, 8081, 9200] and random.random() < 0.2:
            log_event(ip, local_port, "🪞 MIRRORING", f"PEER_{PEER_IP}")
            client_socket.sendall(f"HTTP/1.1 302 Found\r\nLocation: http://{PEER_IP}:{local_port}\r\nServer: MexCapital-Mesh\r\n\r\n".encode())
            return

        log_event(ip, local_port)
        client_socket.sendall(b"MEXCAPITAL_INTERNAL_BREADCRUMB_STALL\n")
        time.sleep(2)
    except: pass
    finally:
        try: client_socket.close()
        except: pass

def start_listener(port):
    if port == 8888: return
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, port))
        server.listen(150)
        while True:
            c, a = server.accept()
            threading.Thread(target=handle_client, args=(c, a, port), daemon=True).start()
    except: pass

if __name__ == "__main__":
    if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR, exist_ok=True)
    print(f"[*] REANIMATING {VERSION}...")
    threading.Thread(target=start_dashboard, daemon=True).start()
    for p in ALL_PORTS:
        threading.Thread(target=start_listener, args=(p,), daemon=True).start()
        time.sleep(1.2)
    print(f"[STATUS] ALL HEADS ONLINE.")
    while True: time.sleep(10)
