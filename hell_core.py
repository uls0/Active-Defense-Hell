import socket
import threading
import time
import os
import binascii
import random
import requests
import base64
import json
import zlib
import signal
import sys
from datetime import datetime
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, mesh_node, predictive_ai, database_emulator, forensics_engine

# CONFIGURACIÓN HELL v8.8.0: AUTOMATED FORENSICS
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
DB_PORTS = [3306, 1433]
PORTS = WEB_PORTS + LETHAL_PORTS + DB_PORTS + [502]
LOG_FILE = "logs/hell_activity.log"

MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs/malware", exist_ok=True)
        os.makedirs("logs/abuse_reports", exist_ok=True)
        os.makedirs("logs/forensics", exist_ok=True)
        self.whitelist = {MY_IP, "127.0.0.1"}
        self.stats = {} 
        self.mesh = mesh_node.start_mesh_service("NODE-SFO-01", [])
        self.ai = predictive_ai.HellPredictiveAI()
        print(f"HELL CORE v8.8.0: Automated Forensics & Evidence Packaging enabled.")

    def log_neutralization(self, ip, duration, bytes_sent, mode, ja3=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        mb_sent = round(bytes_sent / (1024 * 1024), 4)
        
        if ip in self.stats:
            self.stats[ip]['total_time'] += duration
            self.stats[ip]['total_data'] += mb_sent
        
        report = (
            f"[-] THREAT NEUTRALIZED: {timestamp}\n"
            f"    └─ Current Retention: {round(duration, 2)}s | Current Data: {mb_sent}MB\n"
            f"    └─ TOTAL DAMAGE: Time Lost: {round(self.stats[ip]['total_time'], 2)}s | Data Injected: {round(self.stats[ip]['total_data'], 2)}MB\n"
            f"    └─ Final Mitigation: {mode}\n"
            f"----------------------------------------\n"
        )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)
        
        # DISPARAR FORENSE SI EL DAÑO ES ALTO (>300s o >10MB)
        if duration > 300 or mb_sent > 10:
            forensics_engine.create_evidence_pack(ip, timestamp)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        start_time = time.time()
        final_mode = "Mitigation"
        total_bytes = 0
        
        try:
            client_socket.settimeout(10.0)
            data = client_socket.recv(4096)
            req_str = data.decode('utf-8', errors='ignore')

            if "/owa" in req_str or ".zip" in req_str:
                final_mode = "Fifield Bomb"
                zip_generator.serve_zip_trap(client_socket)
                return
            
            if local_port == 22:
                final_mode = "Cowrie Trap"
                shell_emulator.handle_cowrie_trap(client_socket, ip)
                return

            if local_port == 3306:
                final_mode = "MySQL Trap"
                database_emulator.handle_mysql_trap(client_socket)
                return

            # Tarpit genérico
            while True:
                client_socket.send(b"\x00")
                total_bytes += 1
                time.sleep(30)

        except: pass
        finally:
            duration = time.time() - start_time
            self.log_neutralization(ip, duration, total_bytes, final_mode)
            client_socket.close()

    def start(self):
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        for port in PORTS:
            threading.Thread(target=lambda p=port: self.start_listener(p), daemon=True).start()
        print(f"[✅] HELL CORE v8.8.0 (FORENSICS-READY) activo.")
        while True: time.sleep(1)

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

if __name__ == "__main__":
    HellServer().start()
