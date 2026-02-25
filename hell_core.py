import socket
import threading
import time
import os
import json
import random
import requests
import signal
import sys
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine

# CONFIGURACIÓN HELL v9.0.0: THE GREAT WALL & ULTIMATE LOGS
HOST = '0.0.0.0'
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200]
LOG_FILE = "logs/hell_activity.log"
INTEL_FILE = "logs/mesh_intel.json"

MAX_THREADS = 150
SWARM_THRESHOLD = 0.8

class HellServer:
    def __init__(self):
        os.makedirs("logs/forensics", exist_ok=True)
        self.stats = {}
        self.active_threads = 0
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        print(f"💀 HELL CORE v9.0.0: Ultimate Intel & Swarm Active.")

    def get_full_intel(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp", timeout=3).json()
            return f"{r.get('city')}, {r.get('country')}", r.get('as'), r.get('isp')
        except: return "Unknown", "Unknown", "Unknown"

    def log_engagement(self, ip, port, ja3=None, mesh_hit=False):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        loc, asn, isp = self.get_full_intel(ip)
        
        if ip not in self.stats:
            self.stats[ip] = {'hits': 1, 'ports': [port], 'commands': [], 'ja3': ja3, 'total_time': 0, 'total_data': 0}
        else:
            self.stats[ip]['hits'] += 1
            if port not in self.stats[ip]['ports']: self.stats[ip]['ports'].append(port)

        actor, conf = self.profiler.classify_attacker(self.stats[ip]['commands'], ja3, self.stats[ip]['ports'])
        prefix = "[📡 MESH-BLOCK]" if mesh_hit else "[+] ULTIMATE DECEPTION"

        report = (
            f"\n{prefix} TRIGGERED: {timestamp}\n"
            f"----------------------------------------\n"
            f"IP: {ip} | Actor Profile: {actor} ({conf}%)\n"
            f"Origin: {loc} | Network: {isp}\n"
            f"Target Port: {port} | Session Hits: {self.stats[ip]['hits']}\n"
            f"----------------------------------------\n"
        )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)

    def log_neutralization(self, ip, duration, bytes_sent, mode):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        mb_sent = round(bytes_sent / (1024 * 1024), 4)
        if ip in self.stats:
            self.stats[ip]['total_time'] += duration
            self.stats[ip]['total_data'] += mb_sent
        
        report = (
            f"[-] THREAT NEUTRALIZED: {timestamp}\n"
            f"    └─ Current Retention: {round(duration, 2)}s | Data: {mb_sent}MB\n"
            f"    └─ TOTAL DAMAGE: Time Lost: {round(self.stats[ip]['total_time'], 2)}s | Data Injected: {round(self.stats[ip]['total_data'], 2)}MB\n"
            f"    └─ Final Mitigation: {mode}\n"
            f"----------------------------------------\n"
        )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        self.active_threads += 1
        ja3_hash = None
        
        # 1. Swarming check
        if self.active_threads > (MAX_THREADS * SWARM_THRESHOLD):
            # Delegar si el nodo está lleno (Lógica simplificada por desacoplamiento)
            client_socket.send(b"HTTP/1.1 302 Found\r\nLocation: http://127.0.0.1:8888\r\n\r\n")
            self.active_threads -= 1; client_socket.close(); return

        # 2. Intelligence check
        mesh_hit = False
        if os.path.exists(INTEL_FILE):
            with open(INTEL_FILE, 'r') as f:
                intel = json.load(f)
                if ip in intel.get("blacklist_ips", {}): mesh_hit = True

        threading.Thread(target=self.log_engagement, args=(ip, local_port, None, mesh_hit)).start()

        start_time = time.time()
        final_mode = "Mitigation"
        total_bytes = 0

        try:
            client_socket.settimeout(10.0)
            if mesh_hit:
                zip_generator.serve_zip_trap(client_socket)
                return

            # Main Logic
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
                total_bytes += 1
                time.sleep(30)
        except: pass
        finally:
            self.log_neutralization(ip, time.time() - start_time, total_bytes, final_mode)
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
        print(f"[✅] HELL v9.0.0-ULTIMATE Operational.")
        while True: time.sleep(1)

if __name__ == "__main__":
    HellServer().start()
