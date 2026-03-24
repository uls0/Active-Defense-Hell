import socket, time, os, json, re
from collections import Counter

# =============================================================================
# DASHBOARD SERVER v2.2 - HELL LOOT-REPAIR
# =============================================================================

def start_dashboard(log_file="logs/dashboard_live.log"):
    host = '0.0.0.0'
    port = 8888
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    template_path = "templates/dashboard.html"
    loot_file = "logs/credentials.log"

    print(f"[*] DASHBOARD_SERVER v2.2: Operational on port {port}")

    try:
        server.bind((host, port))
        server.listen(50)
        while True:
            client, addr = server.accept()
            try:
                raw_request = client.recv(4096).decode('utf-8', errors='ignore')
                first_line = raw_request.split('\n')[0]
                
                # --- ROUTING LOGIC ---
                
                # 1. ENDPOINT: STATS
                if "/api/stats" in first_line:
                    stats = {"hits": 0, "total_data": 0, "recent_events": [], "botnets": [], "countries": {"RUSSIA": 22, "CHINA": 45, "USA": 31, "MEXICO": 8}}
                    if os.path.exists(log_file):
                        with open(log_file, "r", encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            stats["hits"] = len([l for l in lines if "Hit" in l or "ENGAGED" in l])
                            stats["total_data"] = stats["hits"] * 0.18
                            for l in lines[-20:]:
                                try:
                                    p = l.split("|")
                                    stats["recent_events"].append({
                                        "time": p[0].strip(), "ip": p[1].replace("IP:","").strip(),
                                        "port": p[2].replace("Port:","").strip(), "network": "MEXCAPITAL_API",
                                        "tactic": p[3].replace("State:","").strip()
                                    })
                                except: pass
                    
                    content = json.dumps(stats)
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\nContent-Length: {len(content)}\r\n\r\n{content}"
                    client.sendall(response.encode('utf-8'))
                    return

                # 2. ENDPOINT: LOOT (CREDENTIALS)
                elif "/api/loot" in first_line:
                    loot_data = []
                    if os.path.exists(loot_file):
                        try:
                            with open(loot_file, "r") as f:
                                # Leemos las ultimas 10 lineas y limpiamos
                                raw_lines = f.readlines()
                                loot_data = [l.strip() for l in raw_lines[-10:] if l.strip()]
                        except: pass
                    
                    content = json.dumps({"loot": loot_data})
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\nContent-Length: {len(content)}\r\n\r\n{content}"
                    client.sendall(response.encode('utf-8'))
                    return # Salir tras responder API

                # 3. ENDPOINT: DASHBOARD (HTML)
                else:
                    if os.path.exists(template_path):
                        with open(template_path, "r", encoding="utf-8") as f: content = f.read()
                    else: content = "<h1>ERROR: Template Missing</h1>"
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nConnection: close\r\nContent-Length: {len(content.encode('utf-8'))}\r\n\r\n{content}"
                    client.sendall(response.encode('utf-8'))

            except Exception as e: pass
            finally: client.close()
    except Exception as e: print(f"Fatal: {e}")

if __name__ == "__main__": start_dashboard()
