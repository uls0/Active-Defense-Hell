import os, threading, time, socket, sys, json, random
from elite_deception import EliteHandler
from scripts import dashboard_server

VERSION = "v17.3-HOST-SEQUENTIAL"
LOG_FILE = "logs/hell_activity.log"
HOST = '0.0.0.0'

# Puertos GOLD & ELITE consolidado
GOLD_PORTS = [21, 22, 23, 25, 53, 80, 81, 88, 110, 111, 135, 137, 139, 143, 161, 179, 389, 443, 445, 502, 1433, 3306, 3389]
ELITE_PORTS = [6443, 8080, 2375, 2376, 9100, 9090, 9200, 5601, 6379, 11211, 8081, 3000, 5000, 8000, 11434]
SYSTEM_PORTS = [6666, 8888]

ALL_PORTS = GOLD_PORTS + ELITE_PORTS + SYSTEM_PORTS

class TitanServer:
    def __init__(self):
        print(f"[*] INITIALIZING TITAN {VERSION}")
        os.makedirs("logs", exist_ok=True)
        os.makedirs("payloads", exist_ok=True)
        try:
            self.elite = EliteHandler(self.log_event)
        except Exception as e:
            print(f"[!] Error EliteHandler: {e}")
            self.elite = None

    def log_event(self, ip, port, action="Hit", status="ENGAGED", info=""):
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        report = f"[{action}] {ts} | IP: {ip} | Port: {port} | State: {status} | Info: {info}\n"
        with open(LOG_FILE, "a") as f: f.write(report)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        try:
            if self.elite and local_port in ELITE_PORTS:
                self.elite.dispatch(client_socket, addr, local_port)
                return
            
            # Handler para el VOID (vía puerto 6666)
            if local_port == 6666:
                self.log_event(ip, local_port, "VOID_CAPTURE", "SUMERGIDO")
                client_socket.sendall(b"WELCOME_TO_THE_VOID\n")
                time.sleep(10)
                return

            # Handler Genérico Gold
            self.log_event(ip, local_port)
            client_socket.sendall(b"MEXCAPITAL_STALL_NODE\n")
            time.sleep(2)
        except: pass
        finally:
            try: client_socket.close()
            except: pass

    def start_listener(self, port):
        if port == 8888: return 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(150)
            print(f"[OK] {port} Active")
            while True:
                c, a = server.accept()
                threading.Thread(target=self.handle_client, args=(c, a, port), daemon=True).start()
        except Exception as e:
            print(f"[!] FAIL {port}: {e}")

    def start(self):
        # 1. Dashboard primero
        threading.Thread(target=dashboard_server.start_dashboard, args=(LOG_FILE,), daemon=True).start()
        time.sleep(2)
        
        # 2. Apertura secuencial de puertos
        print(f"[*] Starting sequential boot for {len(ALL_PORTS)} ports...")
        for port in ALL_PORTS:
            if port == 8888: continue
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
            time.sleep(1.5) # Delay de estabilidad
            
        print(f"[STATUS] {VERSION} ONLINE. Full Patrol Active.")
        while True: time.sleep(10)

if __name__ == "__main__":
    TitanServer().start()
