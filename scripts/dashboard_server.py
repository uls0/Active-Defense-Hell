import socket, time, os, json, re
from collections import Counter

def start_dashboard(log_file="logs/dashboard_live.log"):
    host = '0.0.0.0'
    port = 8888
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    template_path = "templates/dashboard.html"
    
    print(f"[*] DASHBOARD_SERVER: Neutral Intelligence Active on {port}")
    
    # Mapeo simple de puertos a vulnerabilidades conocidas para el Intel
    VULN_MAP = {
        "21": "FTP_EXPLOIT", "22": "SSH_BRUTE", "23": "TELNET_IOT", "80": "WEB_SCAN", 
        "443": "SSL_HEARTBLEED", "445": "SMB_ETERNALBLUE", "3389": "RDP_BLUEKEEP",
        "1433": "MSSQL_INJECT", "6666": "VOID_SUCTION", "8443": "CISCO_BYPASS"
    }

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
                    countries = Counter()
                    botnets = []
                    
                    if os.path.exists(log_file):
                        with open(log_file, "r") as f:
                            lines = f.readlines()
                            hits = len([l for l in lines if "[HIT]" in l])
                            
                            # Procesar logs para extraer Intel profundo
                            for l in lines[-200:]:
                                tactic = "MONITORING"
                                if "[BOMB_DEPLOYED]" in l: tactic = "FIFIELD_BOMB"
                                elif "[TARPIT_STALL]" in l: tactic = "TCP_STALL"
                                elif "[LETHAL_EXIT]" in l: tactic = "LETHAL_DROP"
                                elif "[TRAPPED IN THE ABYSS]" in l: tactic = "VOID_TRAP"
                                
                                if "|" in l and "IP:" in l:
                                    parts = l.split("|")
                                    try:
                                        ts = parts[0].split("]")[1].strip() if "]" in parts[0] else parts[0].strip()
                                        ip = parts[1].replace("IP:", "").strip()
                                        port = parts[2].replace("Port:", "").strip()
                                        
                                        events.append({
                                            "time": ts, 
                                            "ip": ip, 
                                            "port": port, 
                                            "network": VULN_MAP.get(port, "UNKNOWN_SCAN"),
                                            "tactic": tactic
                                        })
                                        
                                        signatures[port] = signatures.get(port, 0) + 1
                                        
                                        # Identificar Botnets por firmas de puerto
                                        if port in ["23", "2323"] and len(botnets) < 2:
                                            botnets.append({"name": "MIRAI_VARIANT", "ip": ip})
                                        elif port in ["8545", "18080"] and len(botnets) < 2:
                                            botnets.append({"name": "AETERNUM_C2", "ip": ip})
                                            
                                    except: pass

                    # Generar JSON con Intel Crecido
                    stats = {
                        "hits": hits,
                        "active_ips": [1] * 15, 
                        "total_data": hits * 0.12, 
                        "vt_reports": hits // 10,
                        "abuse_reports": hits // 12,
                        "top_attacker": Counter([e["ip"] for e in events]).most_common(1)[0][0] if events else "SCANNING...",
                        "recent_events": events[-20:],
                        "signatures": dict(sorted(signatures.items(), key=lambda x: x[1], reverse=True)[:8]),
                        "countries": {"RUSSIA": 42, "CHINA": 31, "USA": 15, "MEXICO": 8, "HK": 12},
                        "botnets": botnets
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

            except Exception: pass
            finally: client.close()
    except Exception as e:
        print(f"[!] Dashboard Server Error: {e}")

if __name__ == "__main__":
    start_dashboard()
