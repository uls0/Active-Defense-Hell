import socket
import threading
import time
import os
import sys
import json
import random
import requests
import signal
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing, canary_generator, malware_triage, network_simulator

VERSION = "v10.2.0-CONSOLIDATED"
LOG_FILE = "logs/hell_activity.log"
INTEL_FILE = "logs/mesh_intel.json"
HOST = '0.0.0.0'
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200, 4455]

class HellServer:
    def __init__(self):
        print(f"[*] DEPLOYING {VERSION} | THE ULTIMATE DEFENSE")
        os.makedirs("logs/forensics", exist_ok=True)
        os.makedirs("logs/malware", exist_ok=True)
        self.stats = {}
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def get_full_intel(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp", timeout=2).json()
            return f"{r.get('city')}, {r.get('country')}", r.get('as'), r.get('isp')
        except: return "Unknown", "Unknown", "Unknown"

    def log_engagement(self, ip, port, ja3=None, mesh_hit=False, prediction=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        loc, asn, isp = self.get_full_intel(ip)
        if ip not in self.stats:
            self.stats[ip] = {'hits': 1, 'ports': [port], 'commands': [], 'ja3': ja3, 'total_time': 0, 'total_data': 0}
        else:
            self.stats[ip]['hits'] += 1
            if port not in self.stats[ip]['ports']: self.stats[ip]['ports'].append(port)

        actor, conf = self.profiler.classify_attacker(self.stats[ip]['commands'], ja3, self.stats[ip]['ports'])
        prefix = "[📡 MESH-BLOCK]" if mesh_hit else "[+] TRIGGERED"
        ai_tag = f" [🧠 PREDICTED: {prediction[0]}]" if prediction and prediction[0] else ""
        
        report = (
            f"\n{prefix}: {timestamp}{ai_tag}\n"
            f"IP: {ip} | Actor: {actor}({conf}%)\n"
            f"Origin: {loc} | Network: {isp} | JA3: {ja3 if ja3 else 'N/A'}\n"
            f"Target Port: {port} | Hits: {self.stats[ip]['hits']}\n"
            f"----------------------------------------\n"
        )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)
        print(f"[🔥] {actor} ENGAGED: {ip} on {port}")
        return self.stats[ip]['hits']

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        start_time = time.time()
        
        # 1. AI & JA3
        predicted_port, confidence = self.ai.analyze_sequence(ip, local_port)
        ja3_hash = None
        if local_port in [443, 8443]:
            try: ja3_hash = ja3_engine.get_ja3_hash(client_socket.recv(1024, socket.MSG_PEEK))
            except: pass

        # 2. Mesh Check
        mesh_hit = False
        if os.path.exists(INTEL_FILE):
            try:
                with open(INTEL_FILE, 'r') as f:
                    intel = json.load(f)
                    if ip in intel.get("blacklist_ips", {}) or (ja3_hash and ja3_hash in intel.get("blacklist_ja3", {})):
                        mesh_hit = True
            except: pass

        hit_count = self.log_engagement(ip, local_port, ja3_hash, mesh_hit, (predicted_port, confidence))
        total_bytes = 0
        final_mode = "Mitigation"

        try:
            client_socket.settimeout(10.0)
            if mesh_hit:
                zip_generator.serve_zip_trap(client_socket)
                return

            # --- LÓGICA DE SERVICIOS CONSOLIDADA ---
            data = client_socket.recv(8192)
            req_str = data.decode('utf-8', errors='ignore')

            # Canary Detection
            if "/tracking/beacon.png" in req_str:
                print(f"[🔔] CANARY TRIGGERED: {ip}")
                return

            # Malware Capture (POST/PUT)
            if "POST" in req_str or "PUT" in req_str or b"\x7fELF" in data:
                final_mode = "Malware Captured"
                malware_triage.perform_triage(malware_triage.save_sample(data, ip))
                zip_generator.serve_zip_trap(client_socket)
                return

            # Canary Files
            if "GET /nomina" in req_str or "GET /conf" in req_str:
                final_mode = "Canary Served"
                canary_generator.serve_canary_file(client_socket, "MY_IP", f"NOMINA_{ip}.pdf")
                return

            # Standard Services
            if local_port in [445, 4455]:
                final_mode = "AD-Fake"
                total_bytes = smb_lethal.handle_smb_session(client_socket, ip)
            elif local_port == 22:
                final_mode = "SSH-Bait"
                shell_emulator.handle_cowrie_trap(client_socket, ip, hit_count)
            elif local_port == 3306:
                final_mode = "MySQL-Trap"
                database_emulator.handle_mysql_trap(client_socket)
            elif "/owa" in req_str or ".zip" in req_str:
                final_mode = "Fifield-Bomb"
                zip_generator.serve_zip_trap(client_socket)
            else:
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
                with open(LOG_FILE, "a") as f:
                    f.write(f"[-] NEUTRALIZED: {time.ctime()} | Held: {round(duration,2)}s | Data: {mb}MB | Mode: {final_mode}\n")
                if duration > 60: forensics_engine.create_evidence_pack(ip, time.time())
            client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(500)
            print(f"[✅] Port {port}: ARMED")
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except: pass

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        print(f"[🚀] {VERSION} IS LIVE. THE ULTIMATE DEFENSE SYSTEM.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
