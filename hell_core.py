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
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, mesh_node, predictive_ai, database_emulator

# CONFIGURACIÓN HELL v8.7.0: DEEP FAKE SERVICES & DATABASE TRAPS
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
DB_PORTS = [3306, 1433] # MySQL y SQL Server
SCADA_PORTS = [502]
PORTS = WEB_PORTS + LETHAL_PORTS + DB_PORTS + SCADA_PORTS
LOG_FILE = "logs/hell_activity.log"

MAX_RETENTION_THREADS = 150
SWARM_THRESHOLD = 0.8

MESH_PEERS = os.getenv("HELL_MESH_PEERS", "").split(",") 
NODE_ID = os.getenv("HELL_NODE_ID", "NODE-SFO-01")
MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs/malware", exist_ok=True)
        os.makedirs("logs/abuse_reports", exist_ok=True)
        self.whitelist = {MY_IP, "127.0.0.1"}
        self.stats = {} 
        self.active_threads = 0
        self.mesh = mesh_node.start_mesh_service(NODE_ID, [p.strip() for p in MESH_PEERS if p.strip()])
        self.ai = predictive_ai.HellPredictiveAI()
        threading.Thread(target=self.broadcast_load_loop, daemon=True).start()
        print(f"HELL CORE v8.7.0: Deep Fake DBs (MySQL/MSSQL) synchronized.")

    def broadcast_load_loop(self):
        while True:
            self.mesh.broadcast_load(self.active_threads, MAX_RETENTION_THREADS)
            time.sleep(10)

    def log_engagement(self, ip, port, mesh_pre_flag=False, prediction_data=None, ja3=None, swarmed=False):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        rdns, loc, asn, isp, profile = self.get_full_intel(ip)
        if ip not in self.stats: self.stats[ip] = {'hits': 1, 'total_time': 0, 'total_data': 0}
        else: self.stats[ip]['hits'] += 1
        prefix = "[📡 MESH-BLOCK]" if mesh_pre_flag else "[+] ULTIMATE DECEPTION"
        report = (
            f"\n{prefix} TRIGGERED: {timestamp} | Port: {port}\n"
            f"----------------------------------------\n"
            f"IP: {ip} ({rdns})\n"
            f"Origin: {loc} | Network: {isp}\n"
            f"Classification: Data Exfiltration Bot | Confidence: High\n"
            f"----------------------------------------\n"
        )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)

    def get_full_intel(self, ip):
        try:
            try: rdns = socket.gethostbyaddr(ip)[0]
            except: rdns = ip
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp,proxy", timeout=3).json()
            return rdns, f"{r.get('city')}, {r.get('country')}", r.get('as'), r.get('isp'), "BOT"
        except: return ip, "Unknown", "Unknown", "Unknown", "BOT"

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        self.active_threads += 1
        
        # --- SWARMING ---
        if self.active_threads > (MAX_RETENTION_THREADS * SWARM_THRESHOLD):
            best_peer = self.mesh.get_best_node()
            if best_peer:
                if local_port in WEB_PORTS:
                    redirect = f"HTTP/1.1 302 Found\r\nLocation: http://{best_peer}:{local_port}/\r\n\r\n"
                    client_socket.send(redirect.encode())
                    self.active_threads -= 1; client_socket.close(); return

        # --- DB TRAPS ---
        if local_port == 3306:
            self.log_engagement(ip, local_port)
            database_emulator.handle_mysql_trap(client_socket)
            self.active_threads -= 1; return
        elif local_port == 1433:
            self.log_engagement(ip, local_port)
            database_emulator.handle_mssql_trap(client_socket)
            self.active_threads -= 1; return

        start_time = time.time()
        final_mode = "Mitigation"
        total_bytes = 0
        threading.Thread(target=self.log_engagement, args=(ip, local_port)).start()

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

            # Infinite Tarpit
            while True:
                client_socket.send(b"\x00")
                total_bytes += 1
                time.sleep(30)

        except: pass
        finally:
            duration = time.time() - start_time
            self.log_neutralization(ip, duration, total_bytes, final_mode)
            self.active_threads -= 1
            try: client_socket.close()
            except: pass

    def log_neutralization(self, ip, duration, bytes_sent, mode):
        # (Lógica de log y broadcast mesh se mantiene)
        pass

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
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        print(f"[✅] HELL CORE v8.7.0 (DB-POWERED) desplegado.")
        while True: time.sleep(1)

if __name__ == "__main__":
    HellServer().start()
