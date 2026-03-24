import os, threading, time, socket, sys, json, random, ssl
import base64

# =============================================================================
# HELL CORE v17.5 - NATIVE RANSOMWARE TRAP (MEXCAPITAL)
# =============================================================================

VERSION = "v17.5-RANSOM-READY"
BASE_DIR = "/root/Active-Defense-Hell"
LOG_DIR = f"{BASE_DIR}/logs"
LOG_FILE = f"{LOG_DIR}/hell_activity.log"
LOOT_FILE = f"{LOG_DIR}/credentials.log"
VAULT_DIR = f"{BASE_DIR}/assets/poison_vault"
HOST = '0.0.0.0'

# Arsenal Total: Gold (21-3389) + Elite (6443-11434) + Ransom (2049, 873) + Void (6666)
ALL_PORTS = [21, 22, 23, 25, 53, 80, 81, 88, 110, 111, 135, 137, 139, 143, 161, 179, 389, 443, 445, 502, 1433, 3306, 3389, 6443, 8080, 2375, 2376, 9100, 9090, 9200, 5601, 6379, 11211, 8081, 3000, 5000, 8000, 11434, 6666, 2049, 873]

def log_event(ip, port, action="Hit", status="ENGAGED", info=""):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    if "RANSOM" in info.upper() or "!!!_READ_ME" in info.upper(): action = "🚨 RANSOM_NOTE"
    report = f"[{action}] {ts} | IP: {ip} | Port: {port} | State: {status} | Info: {info}\n"
    if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(report)
        f.flush()
        os.fsync(f.fileno())

def handle_exfiltration(client_socket, ip, port):
    start_time = time.time()
    log_event(ip, port, "📦 EXFIL_START", "MEXCAPITAL_VAULT_OPEN")
    total_bytes = 0
    try:
        if os.path.exists(VAULT_DIR):
            for f_name in os.listdir(VAULT_DIR):
                f_path = os.path.join(VAULT_DIR, f_name)
                if os.path.isfile(f_path) or os.path.islink(f_path):
                    with open(f_path, "rb") as f:
                        while chunk := f.read(1024 * 1024): # 1MB chunks
                            client_socket.sendall(chunk)
                            total_bytes += len(chunk)
        
        duration = time.time() - start_time
        speed = (total_bytes/1024/1024)/duration if duration > 0 else 0
        log_event(ip, port, "🏁 EXFIL_COMPLETE", "POISONED", f"{total_bytes/1024/1024:.2f}MB | {speed:.2f}MB/s")
    except: pass
    finally: client_socket.close()

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
                first_line = raw.split('\n')[0]
                if "/api/stats" in first_line:
                    hits = 0; events = []
                    if os.path.exists(LOG_FILE):
                        with open(LOG_FILE, "r") as f:
                            lines = f.readlines(); hits = len(lines)
                            for l in lines[-20:]:
                                try:
                                    p = l.split("|")
                                    events.append({"time": p[0].strip(), "ip": p[1].replace("IP:","").strip(), "port": p[2].replace("Port:","").strip(), "network": "MEXCAPITAL_AUTO", "tactic": p[3].replace("State:","").strip()})
                                except: pass
                    res = json.dumps({"hits": hits, "total_data": hits*0.18, "recent_events": events, "botnets": [], "countries": {"MX": 10}})
                    client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(res)}\r\n\r\n{res}".encode())
                elif "/api/loot" in first_line:
                    loot = []
                    if os.path.exists(LOOT_FILE):
                        with open(LOOT_FILE, "r") as f: loot = [l.strip() for l in f.readlines()[-10:]]
                    res = json.dumps({"loot": loot})
                    client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(res)}\r\n\r\n{res}".encode())
                else:
                    template_path = f"{BASE_DIR}/templates/dashboard.html"
                    with open(template_path, "r") as f: content = f.read()
                    client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode())
            except: pass
            finally: client.close()
    except: pass

def handle_client(client_socket, addr, local_port):
    ip = addr[0]
    exfil_ports = [22, 2049, 873, 445]
    try:
        if local_port in exfil_ports:
            handle_exfiltration(client_socket, ip, local_port)
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
    threading.Thread(target=start_dashboard, daemon=True).start()
    for p in ALL_PORTS:
        threading.Thread(target=start_listener, args=(p,), daemon=True).start()
        time.sleep(1.2)
    while True: time.sleep(10)
