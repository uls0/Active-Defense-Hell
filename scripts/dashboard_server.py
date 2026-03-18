import socket, time, os, json, re

def start_dashboard(log_file="logs/dashboard_live.log"):
    host = '0.0.0.0'
    port = 8888
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    template_path = "templates/dashboard.html"
    
    print(f"[*] DASHBOARD_SERVER: Active on {host}:{port}")
    
    try:
        server.bind((host, port))
        server.listen(15)
        while True:
            client, addr = server.accept()
            try:
                raw_request = client.recv(2048).decode('utf-8', errors='ignore')

                if "GET /api/stats" in raw_request:
                    hits = 0
                    events = []
                    signatures = {}
                    top_attacker = "SCANNING..."
                    
                    if os.path.exists(log_file):
                        with open(log_file, "r") as f:
                            lines = f.readlines()
                            hits = len([l for l in lines if "[HIT]" in l])
                            
                            # Parsear ultimos 15 eventos
                            for l in lines[-100:]:
                                if "|" in l and "IP:" in l:
                                    parts = l.split("|")
                                    try:
                                        ts = parts[0].split("]")[1].strip() if "]" in parts[0] else parts[0].strip()
                                        ip = parts[1].replace("IP:", "").strip()
                                        port = parts[2].replace("Port:", "").strip()
                                        events.append({"time": ts, "ip": ip, "port": port, "network": "INBOUND_SCAN"})
                                        
                                        # Contar firmas (puertos)
                                        signatures[port] = signatures.get(port, 0) + 1
                                    except: pass
                            
                            # Obtener Top Attacker
                            if events:
                                from collections import Counter
                                ip_list = [e["ip"] for e in events]
                                top_attacker = Counter(ip_list).most_common(1)[0][0]

                    # Generar JSON Real
                    stats = {
                        "hits": hits,
                        "active_ips": [1] * 5, # Placeholder para hilos
                        "total_data": hits * 0.12, # Estimado
                        "vt_reports": hits // 10,
                        "abuse_reports": hits // 12,
                        "top_attacker": top_attacker,
                        "recent_events": events[-15:],
                        "signatures": dict(sorted(signatures.items(), key=lambda x: x[1], reverse=True)[:8]),
                        "countries": {"RUSSIA": 12, "CHINA": 24, "USA": 8, "MEXICO": 5} # Placeholder GEO
                    }
                    
                    content = json.dumps(stats)
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(content)}\r\n\r\n{content}"
                    client.send(response.encode('utf-8'))

                else:
                    if os.path.exists(template_path):
                        with open(template_path, "r", encoding="utf-8") as f:
                            content = f.read()
                    else:
                        content = "<h1>ERROR: Dashboard Template Missing</h1>"

                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(content.encode('utf-8'))}\r\n\r\n{content}"
                    client.send(response.encode('utf-8'))

            except Exception as e:
                pass
            finally:
                client.close()
    except Exception as e:
        print(f"[!] Server Error: {e}")

if __name__ == "__main__":
    start_dashboard()
