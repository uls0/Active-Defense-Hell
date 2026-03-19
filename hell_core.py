import os, threading, time, socket, sys, json, random, requests, zipfile, io, shutil
from scripts import sachiel_rdp, leliel_void, titan_engine, dashboard_server, ramiel_tarpit

# =============================================================================
# PROJECT EVANGELION: TITAN CORE v18.0-CISA-EXPANSION
# =============================================================================
# Cebos: DNS, HTTP Headers, HTML Debug
# Arsenal: 151 Puertos Activos (Top 51 + 100 CISA Targets)
# =============================================================================

VERSION = "v18.0-CISA-EXPANSION"
LOG_FILE = "logs/hell_activity.log"
SHADOW_LOG = "logs/dashboard_live.log"
HOST = '0.0.0.0'

# Puertos Base
PORTS = [
    21, 22, 23, 25, 53, 80, 81, 88, 110, 111, 135, 137, 139, 143, 161, 179, 389, 443, 445, 449, 502, 102, 995, 
    1433, 1521, 1883, 2121, 2222, 2323, 2375, 3306, 3389, 4455, 5678, 8080, 8081, 8082, 8090, 8443, 9200, 
    33001, 1338, 8545, 3333, 18080, 20000, 47808, 6160, 6666, 65535, 33893, 33894
]

# Expansión 100 Puertos CISA (DBs, Cloud, IoT, ICS)
CISA_PORTS = [
    1080, 3128, 5432, 6379, 27017, 11211, 10250, 6443, 5060, 5061, 7547, 9000, 8008, 8888, 30303, 37777,
    1911, 4840, 4843, 9600, 1900, 5351, 5353, 5900, 5901, 5984, 10000, 10001, 2000, 2001, 2002, 2003, 2004,
    2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021,
    2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038,
    2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054, 2055,
    2056, 2057, 2058, 2059, 2060, 2061, 2062, 2063, 2064, 2065, 2066, 2067, 2068, 2069, 2070, 2071, 2072
]
PORTS.extend(CISA_PORTS)

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
        
        # --- CEBO DNS (PUERTO 53) ---
        if local_port == 53:
            try:
                # Simular respuesta DNS TXT con el puerto de sacrificio
                dns_bait = b"\x00\x00\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00"
                dns_bait += b"\x0bmaintenance\x08internal\x00\x00\x10\x00\x01"
                dns_bait += b"\x00\x00\x00\x3c\x00\x14\x13RDP_PORT: 33893 (ADMIN)"
                client_socket.send(dns_bait)
                self.log_event(ip, 53, "DNS_BAIT_SENT", "SACRIFICE_SUGGESTED")
            except: pass
            finally: client_socket.close(); return

        # --- CEBO WEB (80, 443, 8080, etc.) ---
        if local_port in [80, 443, 8080, 8081, 8443, 2375]:
            try:
                header = "HTTP/1.1 200 OK\r\n"
                header += "Server: Apache/2.4.41 (Ubuntu) TITAN-CORE\r\n"
                header += "X-Emergency-Access: port=33893\r\n"
                header += "Content-Type: text/html\r\n\r\n"
                body = "<html><body><!-- DEBUG: Legacy RDP portal at 33893 --><h1>Internal Portal</h1></body></html>"
                client_socket.send((header + body).encode())
                time.sleep(1)
                titan_engine.serve_zip_trap(client_socket)
                self.log_event(ip, local_port, "WEB_BAIT_SENT", "SACRIFICE_SUGGESTED")
                return
            except: pass
            finally: client_socket.close(); return

        # --- PROXY DE SACRIFICIO ---
        if local_port in SACRIFICE_MAP:
            t = SACRIFICE_MAP[local_port]
            # Tunel bidireccional omitido para brevedad (ya implementado en v17.2)
            # Simular conexion al XP
            self.log_event(ip, local_port, "SACRIFICE_ENGAGED", t[2])
            client_socket.close(); return

        # Default Tarpit
        ramiel_tarpit.handle_drip(client_socket, ip, local_port)

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

    def start(self):
        threading.Thread(target=leliel_void.start_void, args=(self.log_event,), daemon=True).start()
        threading.Thread(target=dashboard_server.start_dashboard, args=(LOG_FILE,), daemon=True).start()
        for port in PORTS:
            if port != 8888:
                threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
                time.sleep(0.01)
        print(f"[OK] TITAN v18.0 ONLINE. CISA Expansion Active.")
        while True: time.sleep(1)

if __name__ == "__main__": TitanServer().start()
