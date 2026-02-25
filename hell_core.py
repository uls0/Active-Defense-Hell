import socket
import threading
import time
import os
import sys
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing, canary_generator, malware_triage

print("💀 HELL CORE v9.8.0-ULTIMATE: Malware Triage Active.")

HOST = '0.0.0.0'
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200, 4455]
MALWARE_DIR = "logs/malware"
VT_KEY = os.getenv("VT_API_KEY", "")

class HellServer:
    def __init__(self):
        os.makedirs(MALWARE_DIR, exist_ok=True)
        self.stats = {}
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def capture_malware(self, data, ip):
        ts = int(time.time())
        filepath = f"{MALWARE_DIR}/sample_{ip}_{ts}.bin"
        with open(filepath, "wb") as f: f.write(data)
        # Disparar Triage asíncrono
        threading.Thread(target=malware_triage.perform_triage, args=(filepath, VT_KEY), daemon=True).start()
        return filepath

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        try:
            client_socket.settimeout(10.0)
            data = client_socket.recv(8192) # Buffer más grande para scripts
            req_str = data.decode('utf-8', errors='ignore')

            # --- 1. CAPTURA DE MALWARE (POST/PUT) ---
            if "POST" in req_str or "PUT" in req_str or b"\x7fELF" in data:
                print(f"[☣️] MALWARE UPLOAD ATTEMPT FROM {ip}")
                self.capture_malware(data, ip)
                # Tras capturar, lanzar bomba para "castigar" el bot
                zip_generator.serve_zip_trap(client_socket)
                return

            # --- 2. CANARY / TRACKING ---
            if "/tracking/beacon.png" in req_str:
                canary_generator.serve_canary_file(client_socket, "127.0.0.1", "BEACON") # Simplified
                return

            # --- 3. SERVICIOS ESTÁNDAR ---
            if local_port in [445, 4455]:
                smb_lethal.handle_smb_session(client_socket, ip)
                return
            
            if local_port == 22:
                shell_emulator.handle_cowrie_trap(client_socket, ip)
                return

            # Tarpit
            while True:
                client_socket.send(b"\x00")
                time.sleep(30)
        except: pass
        finally:
            try: client_socket.close()
            except: pass

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(300)
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except: time.sleep(5)

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True: time.sleep(1)

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
