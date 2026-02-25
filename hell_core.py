import socket
import threading
import time
import os
import sys
import json
import random
import requests
import signal
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing, canary_generator
from threat_intel import VirusTotalReporter, AbuseIPDBReporter

# CONFIGURACIÓN HELL v9.7.0: DYNAMIC CANARY INTEGRATION
HOST = '0.0.0.0'
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200, 4455]
LOG_FILE = "logs/hell_activity.log"

MY_PUBLIC_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs/forensics", exist_ok=True)
        self.stats = {}
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()
        print(f"Designed by ULSO+GCLI | HELL CORE v9.7.0 Operational.")

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        try:
            client_socket.settimeout(10.0)
            data = client_socket.recv(4096)
            req_str = data.decode('utf-8', errors='ignore')

            # --- 1. DETECCIÓN DE CANARY PING (BEACON) ---
            if "/tracking/beacon.png" in req_str:
                print(f"\n[🔔!!!] CANARY TRIGGERED! IP REAL DETECTADA: {ip}")
                with open(LOG_FILE, "a") as f:
                    f.write(f"\n[🔔] CANARY ALERT: Document opened by REAL IP: {ip} at {time.ctime()}\n")
                return

            # --- 2. SERVIR CANARY PDF (EN RUTAS SENSIBLES) ---
            if "GET /nomina" in req_str or "GET /confidential" in req_str:
                canary_generator.serve_canary_file(client_socket, MY_PUBLIC_IP, f"NOMINA_CORP_{ip}.pdf")
                return

            # --- 3. SMB / AD LABYRINTH ---
            if local_port in [445, 4455]:
                smb_lethal.handle_smb_session(client_socket, ip)
                return

            # --- 4. ZIP BOMB / OWA ---
            if "/owa" in req_str or ".zip" in req_str:
                zip_generator.serve_zip_trap(client_socket)
                return

            # Tarpit genérico
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
            print(f"[✅] Port {port} armed.")
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except: time.sleep(10)

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True: time.sleep(1)

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
