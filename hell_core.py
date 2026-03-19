import os, threading, time, socket, sys, json, random, requests, zipfile, io, shutil
from scripts import sachiel_rdp, leliel_void, titan_engine, dashboard_server, ramiel_tarpit

# =============================================================================
# PROJECT EVANGELION: TITAN CORE v17.5-BEACON-PROVOKE
# =============================================================================
# Dashboard: 8888 | Sacrifice: 33893-33894
# Táctica: Provocación SSH/Telnet hacia nodos de sacrificio.
# =============================================================================

VERSION = "v17.5-BEACON-PROVOKE"
LOG_FILE = "logs/hell_activity.log"
SHADOW_LOG = "logs/dashboard_live.log"
HOST = '0.0.0.0'

PORTS = [
    21, 22, 23, 25, 53, 80, 81, 88, 110, 111, 135, 137, 139, 143, 161, 179, 389, 443, 445, 449, 502, 102, 995, 
    1433, 1521, 1883, 2121, 2222, 2323, 2375, 3306, 3389, 4455, 5678, 8080, 8081, 8082, 8090, 8443, 9200, 
    33001, 1338, 8545, 3333, 18080, 20000, 47808, 6160, 6666, 65535,
    33893, 33894
]

SACRIFICE_MAP = {
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
        report = f"[{action}] {ts} | IP: {ip} | Port: {port} | State: {status} | Info: {info}\n"
        with open(LOG_FILE, "a") as f: f.write(report)

    def forensic_proxy(self, client_socket, target_host, target_port, node_name, attacker_ip, public_port):
        try:
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.settimeout(5.0)
            target_socket.connect((target_host, target_port))
            # Captura de datos iniciales del bot antes del puente
            self.log_event(attacker_ip, public_port, "SACRIFICE_ENGAGED", node_name, "Deep Forensic Uplink Active")
            
            def pipe(source, dest, direction):
                try:
                    while True:
                        data = source.recv(8192)
                        if not data: break
                        # Loggear payloads de salida del bot (posibles comandos/archivos)
                        if direction == "IN":
                            with open(f"payloads/sacrifice_{attacker_ip}.bin", "ab") as p: p.write(data)
                        dest.sendall(data)
                except: pass
                finally:
                    try: source.close()
                    except: pass
                    try: dest.close()
                    except: pass

            threading.Thread(target=pipe, args=(client_socket, target_socket, "IN"), daemon=True).start()
            threading.Thread(target=pipe, args=(target_socket, client_socket, "OUT"), daemon=True).start()
        except Exception as e:
            self.log_event(attacker_ip, public_port, "SACRIFICE_ERR", node_name, str(e))
            client_socket.close()

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if local_port in SACRIFICE_MAP:
            t = SACRIFICE_MAP[local_port]
            self.forensic_proxy(client_socket, t[0], t[1], t[2], ip, local_port)
            return

        # --- LOGICA DE PROVOCACION (SSH/TELNET) ---
        if local_port in [22, 23, 2222, 2323]:
            try:
                provoke = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1\r\n[ERROR] System Locked. Maintenance via port 33893 (Legacy-RDP).\r\n"
                client_socket.send(provoke.encode())
                time.sleep(1)
                self.log_event(ip, local_port, "PROVOKED", "REDIRECT_SUGGESTED", "Sent RDP redirection bait")
            except: pass
            finally: client_socket.close(); return

        self.log_event(ip, local_port, "HIT")
        try:
            client_socket.settimeout(5.0)
            if local_port == 3389:
                sachiel_rdp.handle_mirage(client_socket, ip)
                return
            if local_port in [80, 443, 8080, 8443]:
                res = "HTTP/1.1 200 OK\r\nServer: TITAN-GW\r\n\r\n<h1>Restricted Access</h1>"
                client_socket.send(res.encode())
                time.sleep(1)
                titan_engine.serve_zip_trap(client_socket)
                return
            ramiel_tarpit.handle_drip(client_socket, ip, local_port)
        except: pass
        finally:
            try: client_socket.close()
            except: pass

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(100)
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except OSError: pass
        finally: server.close()

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
        
        print(f"[OK] TITAN v17.5 ONLINE. Provocation Bait Active.")
        while True: time.sleep(1)

if __name__ == "__main__": TitanServer().start()
