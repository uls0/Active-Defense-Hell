import os, threading, time, socket, sys, json, random, requests, zipfile, io, shutil
from scripts import sachiel_rdp, leliel_void, titan_engine, dashboard_server, ramiel_tarpit

# =============================================================================
# PROJECT EVANGELION: TITAN CORE v19.0-LETHAL-SMB
# =============================================================================
# Táctica: Fake RDP Acceptance + SMB Drip Bomb + Folder Maze
# =============================================================================

VERSION = "v19.0-LETHAL-SMB"
LOG_FILE = "logs/hell_activity.log"
SHADOW_LOG = "logs/dashboard_live.log"
HOST = '0.0.0.0'

# Puertos Base + Intercepción Letal
PORTS = [21, 22, 23, 25, 53, 80, 81, 88, 110, 111, 135, 137, 139, 143, 161, 179, 389, 443, 445, 449, 502, 102, 995, 1433, 1521, 1883, 2121, 2222, 2323, 2375, 3306, 3389, 4455, 5678, 8080, 8081, 8082, 8090, 8443, 9200, 33001, 1338, 8545, 3333, 18080, 20000, 47808, 6160, 6666, 65535, 33893, 33894, 4445]

SACRIFICE_MAP = {
    33893: ("127.0.0.1", 44893, "WINXP_SCADA"),
    33894: ("127.0.0.1", 44894, "WINXP_OFFICE"),
    4445: ("127.0.0.1", 44894, "LETHAL_SMB_VAULT") # Proxy hacia el SMB de WinXP Office
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

    def smb_drip_bomb(self, client_socket, attacker_ip):
        # Enviar basura lenta (10 bytes por segundo) mientras el bot cree que lee el AD
        self.log_event(attacker_ip, 445, "SMB_BOMB_ACTIVE", "DRIP_FEEDING")
        junk = b"0" * 1024
        try:
            while True:
                client_socket.sendall(junk)
                time.sleep(1) # El goteo letal
        except: pass
        finally: client_socket.close()

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        
        # --- FAKE RDP ACCEPTANCE (PUERTO 3389) ---
        if local_port == 3389:
            try:
                # TPKT + X.224 Connection Confirm (Pakete de exito simulado)
                success_rdp = b"\x03\x00\x00\x0b\x06\xd0\x00\x00\x12\x34\x00"
                client_socket.send(success_rdp)
                self.log_event(ip, 3389, "RDP_FAKE_SUCCESS", "REDIRECT_SUGGESTED")
                time.sleep(1)
            except: pass
            finally: client_socket.close(); return

        # --- LETHAL SMB PROXY ---
        if local_port == 4445:
            self.log_event(ip, 445, "SMB_SACRIFICE_INTERCEPTED", "XP_OFFICE")
            threading.Thread(target=self.smb_drip_bomb, args=(client_socket, ip), daemon=True).start()
            return

        if local_port in SACRIFICE_MAP:
            t = SACRIFICE_MAP[local_port]
            self.log_event(ip, local_port, "SACRIFICE_ENGAGED", t[2])
            client_socket.close(); return

        # Resto de trampas...
        ramiel_tarpit.handle_drip(client_socket, ip, local_port)

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(100)
            while True:
                c, a = server.accept()
                threading.Thread(target=self.handle_client, args=(c, a, port), daemon=True).start()
        except OSError: pass

    def start(self):
        threading.Thread(target=sync_shadow_log, daemon=True).start() # Funcion sync omitida aqui por brevedad
        threading.Thread(target=leliel_void.start_void, args=(self.log_event,), daemon=True).start()
        threading.Thread(target=dashboard_server.start_dashboard, args=(LOG_FILE,), daemon=True).start()
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
            time.sleep(0.01)
        print(f"[OK] TITAN v19.0 ONLINE. Lethal SMB and Fake RDP Active.")
        while True: time.sleep(1)

def sync_shadow_log():
    while True:
        try:
            if os.path.exists("logs/hell_activity.log"): 
                shutil.copy2("logs/hell_activity.log", "logs/dashboard_live.log")
        except: pass
        time.sleep(5)

if __name__ == "__main__": TitanServer().start()
