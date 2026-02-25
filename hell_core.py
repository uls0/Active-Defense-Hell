import socket
import threading
import time
import os
import json
import signal
import sys
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine

# CONFIGURACIÓN HELL v8.9.5: PASSIVE INTELLIGENCE CONSUMER
HOST = '0.0.0.0'
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200]
LOG_FILE = "logs/hell_activity.log"
INTEL_FILE = "logs/mesh_intel.json"

class HellServer:
    def __init__(self):
        os.makedirs("logs/forensics", exist_ok=True)
        self.stats = {}
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        print(f"[🛡️] HELL CORE v8.9.5: Passive Intelligence Consumer Active.")

    def check_mesh_intel(self, ip, ja3=None):
        """Consulta la base de datos de inteligencia compartida en disco"""
        if not os.path.exists(INTEL_FILE): return False
        try:
            with open(INTEL_FILE, 'r') as f:
                intel = json.load(f)
                if ip in intel.get("blacklist_ips", {}): return True
                if ja3 and ja3 in intel.get("blacklist_ja3", {}): return True
        except: pass
        return False

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        # 1. Peek para JA3
        ja3_hash = None
        if local_port in [443, 8443]:
            try: ja3_hash = ja3_engine.get_ja3_hash(client_socket.recv(1024, socket.MSG_PEEK))
            except: pass

        # 2. Check de Inmunidad (Mesh Externo)
        if self.check_mesh_intel(ip, ja3_hash):
            print(f"[📡] MESH-HIT: Destrucción inmediata para {ip}")
            if local_port in [22, 2222]: shell_emulator.terminal_crusher(client_socket)
            else: zip_generator.serve_zip_trap(client_socket)
            return

        # 3. Lógica de Combate Estándar
        try:
            client_socket.settimeout(10.0)
            data = b""; req_str = ""
            try: 
                data = client_socket.recv(4096)
                req_str = data.decode('utf-8', errors='ignore')
            except: pass

            if local_port in [445, 4455]:
                smb_lethal.handle_smb_session(client_socket, ip)
                return
            if "/owa" in req_str or ".zip" in req_str:
                zip_generator.serve_zip_trap(client_socket)
                return
            if local_port == 22:
                shell_emulator.handle_cowrie_trap(client_socket, ip)
                return
            if local_port == 3306:
                database_emulator.handle_mysql_trap(client_socket)
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
            server.listen(100)
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except: pass

    def start(self):
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        for port in PORTS:
            threading.Thread(target=lambda p=port: self.start_listener(p), daemon=True).start()
        print(f"[✅] HELL CORE v8.9.5 Operational on {len(PORTS)} ports.")
        while True: time.sleep(1)

if __name__ == "__main__":
    HellServer().start()
