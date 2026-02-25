import socket
import threading
import time
import os
import sys
import json
import random
import requests
import signal
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing

print("💀 HELL CORE v9.4.0-MASTER-PIECE: Final Engagement Logic Active.")

HOST = '0.0.0.0'
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200]
LOG_FILE = "logs/hell_activity.log"
INTEL_FILE = "logs/mesh_intel.json"

class HellServer:
    def __init__(self):
        os.makedirs("logs/forensics", exist_ok=True)
        self.stats = {} # {ip: {'hits': X, 'ports': [], 'start_time': T, 'total_data': 0}}
        self.active_threads = 0
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        
        # Iniciar monitores de salud y mantenimiento
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()
        print("[✅] All defensive sub-systems synchronized.")

    def get_full_intel(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp", timeout=3).json()
            return f"{r.get('city')}, {r.get('country')}", r.get('as'), r.get('isp')
        except: return "Unknown", "Unknown", "Unknown"

    def log_engagement(self, ip, port, ja3=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        loc, asn, isp = self.get_full_intel(ip)
        
        if ip not in self.stats:
            self.stats[ip] = {'hits': 1, 'ports': [port], 'commands': [], 'ja3': ja3, 'total_time': 0, 'total_data': 0}
        else:
            self.stats[ip]['hits'] += 1
            if port not in self.stats[ip]['ports']: self.stats[ip]['ports'].append(port)

        actor, conf = self.profiler.classify_attacker(self.stats[ip]['commands'], ja3, self.stats[ip]['ports'])
        
        # Verificar Mesh Intel en disco
        mesh_hit = False
        if os.path.exists(INTEL_FILE):
            with open(INTEL_FILE, 'r') as f:
                if ip in json.load(f).get("blacklist_ips", {}): mesh_hit = True

        prefix = "[📡 MESH-BLOCK]" if mesh_hit else "[+] ULTIMATE DECEPTION"
        
        report = (
            f"\n{prefix} TRIGGERED: {timestamp}\n"
            f"----------------------------------------\n"
            f"IP: {ip} | Actor: {actor} ({conf}%)\n"
            f"Origin: {loc} | ISP: {isp}\n"
            f"Target Port: {port} | Hits: {self.stats[ip]['hits']}\n"
            f"Status: BAIT-SWITCH ACTIVE\n"
            f"----------------------------------------\n"
        )
        print(f"[🔥] {actor} ENGAGED on port {port} from {ip}")
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)
        return self.stats[ip]['hits']

    def log_neutralization(self, ip, duration, bytes_sent, mode):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        mb_sent = round(bytes_sent / (1024 * 1024), 4)
        if ip in self.stats:
            self.stats[ip]['total_time'] += duration
            self.stats[ip]['total_data'] += mb_sent
        
        report = (
            f"[-] THREAT NEUTRALIZED: {timestamp}\n"
            f"    └─ Current Retention: {round(duration, 2)}s | Data: {mb_sent}MB\n"
            f"    └─ TOTAL DAMAGE: Time Lost: {round(self.stats[ip]['total_time'], 2)}s | Injected: {round(self.stats[ip]['total_data'], 2)}MB\n"
            f"    └─ Final Mitigation: {mode}\n"
            f"----------------------------------------\n"
        )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        self.active_threads += 1
        hit_count = self.log_engagement(ip, local_port)
        
        start_time = time.time()
        final_mode = "Mitigation"
        total_bytes = 0

        try:
            client_socket.settimeout(15.0)
            
            # --- 1. ACTIVE DIRECTORY (445) ---
            if local_port in [445, 4455]:
                final_mode = "AD-Fake Labyrinth"
                smb_lethal.handle_smb_session(client_socket, ip)
                return

            # --- 2. SSH BAIT & SWITCH (22) ---
            if local_port == 22:
                final_mode = "Cowrie Bait & Switch"
                shell_emulator.handle_cowrie_trap(client_socket, ip, hit_count)
                return

            # --- 3. MAINFRAME (2222) ---
            if local_port == 2222:
                final_mode = "Mainframe Monex"
                shell_emulator.handle_mainframe_shell(client_socket, ip)
                return

            # --- 4. DATA EXFILTRATION (3306) ---
            if local_port == 3306:
                final_mode = "MySQL Data Bomb"
                database_emulator.handle_mysql_trap(client_socket)
                return

            # --- 5. GENERIC TARPIT (RESTO) ---
            while True:
                client_socket.send(b"\x00")
                total_bytes += 1024
                time.sleep(30)

        except: pass
        finally:
            self.log_neutralization(ip, time.time() - start_time, total_bytes, final_mode)
            self.active_threads -= 1
            try: client_socket.close()
            except: pass

    def start_listener(self, port):
        while True:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                server.bind((HOST, port))
                server.listen(250)
                print(f"[✅] Port {port} is ARMED.")
                while True:
                    client, addr = server.accept()
                    threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
            except: time.sleep(10)

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        print(f"[🚀] HELL v9.4.0: SOBERANÍA DIGITAL ALCANZADA. 15 PUERTOS ACTIVOS.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
