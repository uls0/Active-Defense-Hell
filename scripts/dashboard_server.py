import socket, time, os

def start_dashboard(log_file):
    host = '0.0.0.0'
    port = 65535
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((host, port))
        server.listen(5)
        while True:
            client, addr = server.accept()
            try:
                if os.path.exists(log_file):
                    with open(log_file, "r") as f: logs = f.readlines()[-40:]
                else: logs = ["Sin telemetria aun."]
                res = "HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n"
                res += "--- HELL TITAN DASHBOARD v16.0 (DOCKER-HOST) ---\n\n"
                res += "".join(logs)
                client.send(res.encode('utf-8'))
            except: pass
            finally: client.close()
    except: pass
