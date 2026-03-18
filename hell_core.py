import os, threading, time, socket, sys, json, random, requests, zipfile, io
from scripts import sachiel_rdp, leliel_void, titan_engine, dashboard_server, ramiel_tarpit

# =============================================================================
# PROJECT EVANGELION: TITAN CORE v16.2-FORENSIC
# =============================================================================
# Telemetría avanzada para check_hell.
# Dashboard: 65535 | VOID: 20101-65534
# =============================================================================

VERSION = "v16.2-FORENSIC-DOCKER"
LOG_FILE = "logs/hell_activity.log"
HOST = '0.0.0.0'
DASH_PORT = 65535

PORTS = [
    21, 22, 23, 25, 53, 80, 81, 88, 110, 111, 135, 137, 139, 143, 161, 179, 389, 443, 445, 449, 502, 102, 995, 
    1433, 1521, 1883, 2121, 2222, 2323, 2375, 3306, 3389, 4455, 5678, 8080, 8081, 8082, 8090, 8443, 9200, 
    33001, 1338, 8545, 3333, 18080, 20000, 47808, 6160
]
PORTS.extend(range(20000, 20101))

class TitanServer:
    def __init__(self):
        print(f"[*] INITIALIZING TITAN FORENSIC {VERSION}")
        os.makedirs("logs", exist_ok=True)
        os.makedirs("payloads", exist_ok=True)
        titan_engine.precompute_bombs()

    def log_event(self, ip, port, action="Hit", status="ENGAGED"):
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        # Marcadores para check_hell
        marker = f"[{action}]"
        report = f"\n{marker} {ts} | IP: {ip} | Port: {port} | State: {status}\n"
        with open(LOG_FILE, "a") as f: f.write(report)
        print(f"[+] {action}: {ip}:{port}")

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        self.log_event(ip, local_port, "HIT")
        try:
            client_socket.settimeout(10.0)
            
            # --- SACHIEL: MIRAGE RDP ---
            if local_port == 3389:
                self.log_event(ip, local_port, "MIRAGE_ENGAGED")
                sachiel_rdp.handle_mirage(client_socket, ip)
                return

            # --- MATARAEL: Trend Ports (Bombas) ---
            if local_port in [80, 443, 8080, 8443, 5678, 8081, 2375]:
                res = "HTTP/1.1 200 OK\r\nServer: TITAN-GATEWAY\r\n\r\n<h1>Restringido</h1>"
                client_socket.send(res.encode())
                time.sleep(2)
                self.log_event(ip, local_port, "BOMB_DEPLOYED")
                titan_engine.serve_zip_trap(client_socket)
                return

            # --- RAMIEL: Tarpit / Greasy SMB ---
            if local_port in [445, 4455, 139]:
                self.log_event(ip, local_port, "TARPIT_STALL")
                ramiel_tarpit.handle_drip(client_socket, ip, local_port)
                self.log_event(ip, local_port, "LETHAL_EXIT", "KILLED")
                return

            # Default Tarpit
            ramiel_tarpit.handle_drip(client_socket, ip, local_port)
        except: pass
        finally: client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port)); server.listen(500)
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except: pass

    def start(self):
        threading.Thread(target=leliel_void.start_void, args=(self.log_event,), daemon=True).start()
        threading.Thread(target=dashboard_server.start_dashboard, args=(LOG_FILE,), daemon=True).start()
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
            time.sleep(0.005)
        print(f"[✅] TITAN FORENSIC ONLINE.")
        while True: time.sleep(1)

if __name__ == "__main__":
    TitanServer().start()
