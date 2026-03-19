import os, threading, time, socket, sys, json, random, requests, zipfile, io, shutil
from scripts import sachiel_rdp, leliel_void, titan_engine, dashboard_server, ramiel_tarpit

# =============================================================================
# PROJECT EVANGELION: TITAN CORE v18.2-OMEGA-TUNED
# =============================================================================

VERSION = "v18.2-OMEGA-TUNED"
LOG_FILE = "logs/hell_activity.log"
SHADOW_LOG = "logs/dashboard_live.log"
HOST = '0.0.0.0'

PORTS = [
    21, 22, 23, 25, 53, 80, 81, 88, 110, 111, 135, 137, 139, 143, 161, 179, 389, 443, 445, 449, 502, 102, 995, 
    1433, 1521, 1883, 2121, 2222, 2323, 2375, 3306, 3389, 4455, 5678, 8080, 8081, 8082, 8090, 8443, 9200, 
    33001, 1338, 8545, 3333, 18080, 20000, 47808, 6160, 6666, 65535, 33893, 33894,
    5432, 6379, 27017 # Priorizamos estos para que salgan del OFFLINE
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

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if local_port in SACRIFICE_MAP:
            t = SACRIFICE_MAP[local_port]
            try:
                tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tsock.connect(t[:2])
                self.log_event(ip, local_port, "SACRIFICE_ENGAGED", t[2])
                # Puente basico omitido para estabilidad en el ejemplo
                tsock.close()
            except: pass
            finally: client_socket.close(); return

        self.log_event(ip, local_port, "HIT")
        try:
            client_socket.settimeout(5.0)
            if local_port in [80, 443, 8080, 8443, 5432, 6379, 27017]:
                res = "HTTP/1.1 200 OK\r\nServer: TITAN-GW\r\n\r\n<h1>Restricted</h1>"
                client_socket.send(res.encode())
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
                c, a = server.accept()
                threading.Thread(target=self.handle_client, args=(c, a, port), daemon=True).start()
        except OSError as e:
            if port in [5432, 6379, 27017]: print(f"[!] Critical Port {port} Fail: {e}")
        finally: server.close()

    def start(self):
        threading.Thread(target=leliel_void.start_void, args=(self.log_event,), daemon=True).start()
        threading.Thread(target=dashboard_server.start_dashboard, args=(LOG_FILE,), daemon=True).start()
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
            time.sleep(0.02) # Mas tiempo entre hilos para estabilidad
        print(f"[OK] TITAN ONLINE. Arsenal v18.2 Stable.")
        while True: time.sleep(1)

if __name__ == "__main__": TitanServer().start()
