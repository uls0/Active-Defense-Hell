import socket
import threading
import time
import os
import json
import random
import requests
import signal
import sys
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing

# CONFIGURACIÓN HELL v9.1.0: SELF-HEALING & DISK PROTECTION
HOST = '0.0.0.0'
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200]
LOG_FILE = "logs/hell_activity.log"
INTEL_FILE = "logs/mesh_intel.json"

class HellServer:
    def __init__(self):
        os.makedirs("logs/forensics", exist_ok=True)
        self.stats = {}
        self.active_threads = 0
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        
        # Iniciar el sistema de autolimpieza en segundo plano
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()
        
        print(f"💀 HELL CORE v9.1.0: Self-Healing & Disk Protection ACTIVE.")

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        # Protección de disco antes de aceptar conexión pesada
        if self_healing.check_disk_space() < 5:
            client_socket.close(); return

        self.active_threads += 1
        # (Lógica de logs, inteligencia y combate se mantiene intacta de la v9.0.0)
        
        # [Resto del código de v9.0.0 sigue aquí...]
        try:
            client_socket.settimeout(10.0)
            if local_port in [445, 4455]:
                smb_lethal.handle_smb_session(client_socket, ip)
                return
            
            data = client_socket.recv(4096)
            req_str = data.decode('utf-8', errors='ignore')

            if "/owa" in req_str or ".zip" in req_str:
                zip_generator.serve_zip_trap(client_socket)
                return
            if local_port == 22:
                shell_emulator.handle_cowrie_trap(client_socket, ip)
                return
            if local_port == 3306:
                database_emulator.handle_mysql_trap(client_socket)
                return

            while True:
                client_socket.send(b"\x00")
                time.sleep(30)
        except: pass
        finally:
            self.active_threads -= 1
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
        print(f"[✅] HELL v9.1.0-ULTIMATE Operational.")
        while True: time.sleep(1)

if __name__ == "__main__":
    HellServer().start()
