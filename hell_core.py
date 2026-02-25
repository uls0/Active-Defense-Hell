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
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine

# Try to import mesh_node optionally
try: from scripts import mesh_node
except ImportError: mesh_node = None

# CONFIGURACIÓN HELL v8.9.4: MODULAR & EXTERNAL MESH
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389]
DB_PORTS = [3306, 1433]
AD_PORTS = [445, 4455, 389, 88]
PORTS = WEB_PORTS + LETHAL_PORTS + DB_PORTS + AD_PORTS + [502]
LOG_FILE = "logs/hell_activity.log"

MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs/malware", exist_ok=True)
        os.makedirs("logs/abuse_reports", exist_ok=True)
        os.makedirs("logs/forensics", exist_ok=True)
        self.whitelist = {MY_IP, "127.0.0.1"}
        self.stats = {} 
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        
        # Mesh is now strictly OPTIONAL
        self.mesh = None
        if mesh_node and os.getenv("ENABLE_MESH", "false").lower() == "true":
            peers = [p.strip() for p in os.getenv("HELL_MESH_PEERS", "").split(",") if p.strip()]
            self.mesh = mesh_node.start_mesh_service(os.getenv("HELL_NODE_ID", "NODE-01"), peers)
            print("[📡] Mesh Network Integrated and Active.")
        else:
            print("[🛡️] Running in Standalone Mode (Mesh Disabled).")

    def get_full_intel(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp", timeout=3).json()
            return ip, f"{r.get('city')}, {r.get('country')}", r.get('as'), r.get('isp')
        except: return ip, "Unknown", "Unknown", "Unknown"

    def log_engagement(self, ip, port, ja3=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        rdns, loc, asn, isp = self.get_full_intel(ip)
        
        if ip not in self.stats:
            self.stats[ip] = {'hits': 1, 'ports': [port], 'commands': [], 'ja3': ja3, 'start_time': time.time()}
        else:
            self.stats[ip]['hits'] += 1
            if port not in self.stats[ip]['ports']: self.stats[ip]['ports'].append(port)

        actor_type, conf = self.profiler.classify_attacker(self.stats[ip]['commands'], ja3, self.stats[ip]['ports'])

        report = (
            f"\n[+] ULTIMATE DECEPTION TRIGGERED: {timestamp}\n"
            f"----------------------------------------\n"
            f"IP: {ip} ({rdns})\n"
            f"Origin: {loc} | Actor Profile: {actor_type} ({conf}%)\n"
            f"Network: {isp} ({asn})\n"
            f"Target Port: {port} | Hits: {self.stats[ip]['hits']}\n"
            f"----------------------------------------\n"
        )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        ja3_hash = None
        if local_port in [443, 8443]:
            try:
                peek_data = client_socket.recv(1024, socket.MSG_PEEK)
                ja3_hash = ja3_engine.get_ja3_hash(peek_data)
            except: pass

        threading.Thread(target=self.log_engagement, args=(ip, local_port, ja3_hash)).start()

        try:
            client_socket.settimeout(10.0)
            data = b""; req_str = ""
            try: 
                data = client_socket.recv(4096)
                req_str = data.decode('utf-8', errors='ignore')
            except: pass

            # Decision Logic
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
        print(f"[✅] HELL CORE v8.9.4 Operational.")
        while True: time.sleep(1)

if __name__ == "__main__":
    HellServer().start()
