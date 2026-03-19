import os, threading, time, socket, sys, json, random, requests, zipfile, io, shutil
from scripts import sachiel_rdp, leliel_void, titan_engine, dashboard_server, ramiel_tarpit

# =============================================================================
# PROJECT EVANGELION: TITAN CORE v17.2-SACRIFICE-FORENSIC
# =============================================================================

VERSION = "v17.2-SACRIFICE-FORENSIC"
LOG_FILE = "logs/hell_activity.log"
SHADOW_LOG = "logs/dashboard_live.log"
HOST = '0.0.0.0'

# Puertos Emulados + Puertos de Sacrificio
PORTS = [
    21, 22, 23, 25, 53, 80, 81, 88, 110, 111, 135, 137, 139, 143, 161, 179, 389, 443, 445, 449, 502, 102, 995, 
    1433, 1521, 1883, 2121, 2222, 2323, 2375, 3306, 3389, 4455, 5678, 8080, 8081, 8082, 8090, 8443, 9200, 
    33001, 1338, 8545, 3333, 18080, 20000, 47808, 6160, 6666, 65535,
    33891, 33892, 33893, 33894 # Puertos de Sacrificio Interceptados
]

# Mapa de Redireccion Forense (Público -> Interno)
SACRIFICE_MAP = {
    33891: ("127.0.0.1", 44891, "WIN7_ACCOUNTING"),
    33892: ("127.0.0.1", 44892, "WIN7_DEVELOPER"),
    33893: ("127.0.0.1", 44893, "WINXP_SCADA"),
    33894: ("127.0.0.1", 44894, "WINXP_OFFICE")
}

class TitanServer:
    def __init__(self):
        print(f"[*] INITIALIZING TITAN {VERSION}")
        os.makedirs("logs", exist_ok=True)
        os.makedirs("payloads", exist_ok=True)
        titan_engine.precompute_bombs()

    def log_event(self, ip, port, action="Hit", status="ENGAGED", info=""):
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        report = f"\n[{action}] {ts} | IP: {ip} | Port: {port} | State: {status} | Info: {info}\n"
        with open(LOG_FILE, "a") as f: f.write(report)

    def forensic_proxy(self, client_socket, target_host, target_port, node_name, attacker_ip, public_port):
        # Captura de primer contacto (Handshake)
        try:
            initial_payload = client_socket.recv(4096)
            self.log_event(attacker_ip, public_port, "SACRIFICE_ENGAGED", node_name, f"Payload: {initial_payload[:32].hex()}")
            
            # Conectar al Windows Real
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.connect((target_host, target_port))
            target_socket.send(initial_payload)
            
            # Puente bidireccional
            def pipe(source, dest):
                try:
                    while True:
                        data = source.recv(4096)
                        if not data: break
                        dest.send(data)
                except: pass
                finally: 
                    source.close()
                    dest.close()

            threading.Thread(target=pipe, args=(client_socket, target_socket), daemon=True).start()
            threading.Thread(target=pipe, args=(target_socket, client_socket), daemon=True).start()
        except Exception as e:
            self.log_event(attacker_ip, public_port, "SACRIFICE_ERROR", node_name, str(e))
            client_socket.close()

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        
        # --- LOGICA DE SACRIFICIO (PROXY) ---
        if local_port in SACRIFICE_MAP:
            target = SACRIFICE_MAP[local_port]
            self.forensic_proxy(client_socket, target[0], target[1], target[2], ip, local_port)
            return

        # --- LOGICA DE TRAMPAS ESTANDAR ---
        self.log_event(ip, local_port, "HIT")
        try:
            client_socket.settimeout(10.0)
            if local_port == 3389:
                sachiel_rdp.handle_mirage(client_socket, ip)
                return
            if local_port in [80, 443, 8080, 8443, 5678, 8081]:
                res = "HTTP/1.1 200 OK\r\nServer: TITAN-GATEWAY\r\n\r\n<h1>Restringido</h1>"
                client_socket.send(res.encode())
                time.sleep(2)
                self.log_event(ip, local_port, "BOMB_DEPLOYED")
                titan_engine.serve_zip_trap(client_socket)
                return
            ramiel_tarpit.handle_drip(client_socket, ip, local_port)
        except: pass
        finally: client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(500)
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except OSError: pass

    def start(self):
        def sync_logs():
            while True:
                try:
                    if os.path.exists(LOG_FILE): shutil.copy2(LOG_FILE, SHADOW_LOG)
                except: pass
                time.sleep(5)
        
        threading.Thread(target=sync_logs, daemon=True).start()
        threading.Thread(target=leliel_void.start_void, args=(self.log_event,), daemon=True).start()
        threading.Thread(target=dashboard_server.start_dashboard, args=(LOG_FILE,), daemon=True).start()
        
        for port in PORTS:
            if port != 8888:
                threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
                time.sleep(0.01)
        
        print(f"[OK] TITAN FORENSIC v17.2 ONLINE. Sacrifice Grid Active.")
        while True: time.sleep(1)

if __name__ == "__main__": TitanServer().start()
