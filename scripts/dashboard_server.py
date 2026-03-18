import socket, time, os

def start_dashboard(log_file="logs/dashboard_live.log"):
    host = '0.0.0.0'
    port = 8888
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    template_path = "templates/dashboard.html"
    
    print(f"[*] DASHBOARD_SERVER: Listening on {host}:{port} (Reading from {log_file})")
    
    try:
        server.bind((host, port))
        server.listen(10)
        while True:
            client, addr = server.accept()
            try:
                # Aumentar buffer para peticiones largas
                raw_request = client.recv(2048).decode('utf-8', errors='ignore')

                # Endpoint para la API de stats que usa el nuevo Dashboard
                if "GET /api/stats" in raw_request:
                    # Generar JSON de stats simplificado desde el shadow log
                    hits = 0
                    if os.path.exists(log_file):
                        with open(log_file, "r") as f:
                            data = f.read()
                            hits = data.count("[HIT]")
                    
                    content = f'{{"hits": {hits}, "active_ips": [], "total_data": 0, "vt_reports": 0, "abuse_reports": 0, "top_attacker": "LIVE", "recent_events": [], "signatures": {{}}, "countries": {{}}}}'
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nContent-Length: {len(content)}\r\n\r\n{content}"
                    client.send(response.encode('utf-8'))

                # Servir el Dashboard principal
                else:
                    if os.path.exists(template_path):
                        with open(template_path, "r", encoding="utf-8") as f:
                            content = f.read()
                    else:
                        content = "<h1>ERROR: Dashboard Template Missing</h1>"

                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(content.encode('utf-8'))}\r\n\r\n{content}"
                    client.send(response.encode('utf-8'))

            except Exception as e:
                print(f"[!] Dashboard Request Error: {e}")
            finally:
                client.close()
    except Exception as e:
        print(f"[!] Dashboard Server Error: {e}")

if __name__ == "__main__":
    # Si se ejecuta directo, busca el log por defecto
    start_dashboard()
