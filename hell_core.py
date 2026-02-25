import socket
import threading
import time
import os
import sys
import json
import random
import requests
import signal
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing, canary_generator, malware_triage, bgp_emulator, network_simulator

VERSION = "v9.1.0-STABLE-COMPLETE"
LOG_FILE = "logs/hell_activity.log"
HOST = '0.0.0.0'
PORTS = [22, 80, 443, 445, 88, 179, 389, 502, 1433, 2222, 3306, 3389, 4455, 8080, 8443, 9200]

MY_PUBLIC_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        print(f"[*] INITIALIZING {VERSION} | THE PURE SINGULARITY")
        os.makedirs("logs/forensics", exist_ok=True)
        os.makedirs("logs/malware", exist_ok=True)
        self.stats = {}
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def get_full_intel(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp,proxy", timeout=1.2).json()
            return f"{r.get('city')}, {r.get('country')}", r.get('as'), r.get('isp'), "BOT"
        except: return "Unknown", "Unknown", "Unknown", "BOT"

    def log_engagement(self, ip, port, ja3=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        def background_log():
            loc, asn, isp, profile = self.get_full_intel(ip)
            if ip not in self.stats:
                self.stats[ip] = {'hits': 1, 'ports': [port], 'commands': [], 'ja3': ja3, 'total_time': 0, 'total_data': 0}
            else:
                self.stats[ip]['hits'] += 1
            
            actor, conf = self.profiler.classify_attacker(self.stats[ip]['commands'], ja3, self.stats[ip]['ports'])
            report = f"\n[+] ULTIMATE DECEPTION TRIGGERED: {timestamp}\n----------------------------------------\nIP: {ip}\nOrigin: {loc} | Actor: {actor}({conf}%)\nNetwork: {isp} ({asn})\nTarget Port: {port} | Hits: {self.stats[ip]['hits']}\n----------------------------------------\n"
            with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)
            print(f"[🔥] {actor} ENGAGED: {ip} on port {port}")
        threading.Thread(target=background_log, daemon=True).start()

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        start_time = time.time()
        self.log_engagement(ip, local_port)
        total_bytes = 0
        final_mode = "Mitigation"

        try:
            client_socket.settimeout(15.0)
            # Peek para datos iniciales
            try: data = client_socket.recv(4096); req_str = data.decode('utf-8', errors='ignore')
            except: data = b""; req_str = ""

            # --- ROUTING DE SERVICIOS ---
            if "/tracking/beacon.png" in req_str:
                print(f"[🔔] CANARY TRIGGERED: {ip}")
                return

            if "GET /nomina" in req_str or "GET /conf" in req_str:
                canary_generator.serve_canary_file(client_socket, MY_PUBLIC_IP, f"NOMINA_{ip}.pdf")
                final_mode = "Canary-Served"
                return

            if local_port == 22:
                shell_emulator.handle_cowrie_trap(client_socket, ip)
                total_bytes = 4 * 1024 * 1024
                final_mode = "SSH-GigaBomb"
                return

            if local_port in [445, 4455]:
                total_bytes = smb_lethal.handle_smb_session(client_socket, ip)
                final_mode = "AD-Maze"
                return

            if local_port == 3306:
                total_bytes = database_emulator.handle_mysql_trap(client_socket)
                final_mode = "MySQL-Bomb"
                return

            # Tarpit genérico
            while True:
                client_socket.send(b"\x00")
                total_bytes += 1024; time.sleep(30)
        except: pass
        finally:
            duration = time.time() - start_time
            mb = round(total_bytes / (1024*1024), 4)
            if ip in self.stats:
                self.stats[ip]['total_time'] += duration
                self.stats[ip]['total_data'] += mb
                report = f"[-] THREAT NEUTRALIZED: {time.ctime()}\n    └─ Held: {round(duration, 2)}s | Data: {mb}MB | Mode: {final_mode}\n    └─ TOTAL DAMAGE: Data Injected: {round(self.stats[ip]['total_data'], 2)}MB\n----------------------------------------\n"
                with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)
            client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(500)
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except: pass

    def start(self):
        for port in PORTS: threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        print(f"[🚀] {VERSION} IS ACTIVE. TOTAL DEFENSE CONSOLIDATED.")
        while True:
            try: time.sleep(1)
            except: break

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
