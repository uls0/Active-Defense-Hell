import socket
import threading
import time
import os
import sys
import json
import random
import requests
import signal
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing, canary_generator, malware_triage, network_simulator, bgp_emulator

VERSION = "v10.5.3-FINAL-STABLE"
LOG_FILE = "logs/hell_activity.log"
HOST = '0.0.0.0'
# Arsenal de 16 Puertos Armados
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 179, 502, 8080, 8443, 9200, 4455]

MY_PUBLIC_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        print(f"[*] INITIALIZING {VERSION} | THE UNSTOPPABLE CORE")
        os.makedirs("logs/forensics", exist_ok=True)
        os.makedirs("logs/malware", exist_ok=True)
        self.stats = {}
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def get_full_intel(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp", timeout=1.5).json()
            return f"{r.get('city')}, {r.get('country')}", r.get('as'), r.get('isp')
        except: return "Unknown", "Unknown", "Unknown"

    def log_engagement(self, ip, port, ja3=None, prediction=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        def background_log():
            loc, asn, isp = self.get_full_intel(ip)
            if ip not in self.stats:
                self.stats[ip] = {'hits': 1, 'ports': [port], 'commands': [], 'ja3': ja3, 'total_time': 0, 'total_data': 0}
            else:
                self.stats[ip]['hits'] += 1
                if port not in self.stats[ip]['ports']: self.stats[ip]['ports'].append(port)
            
            actor, conf = self.profiler.classify_attacker(self.stats[ip]['commands'], ja3, self.stats[ip]['ports'])
            report = f"\n[+] TRIGGERED: {timestamp}\nIP: {ip} | Actor: {actor}({conf}%)\nOrigin: {loc} | Port: {port}\n----------------------------------------\n"
            with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)
            print(f"[🔥] {actor} ENGAGED: {ip} on {port}")
        threading.Thread(target=background_log, daemon=True).start()

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        start_time = time.time()
        ja3_hash = None
        if local_port in [443, 8443]:
            try: ja3_hash = ja3_engine.get_ja3_hash(client_socket.recv(1024, socket.MSG_PEEK))
            except: pass

        self.log_engagement(ip, local_port, ja3_hash)
        total_bytes = 0
        final_mode = "Mitigation"

        try:
            client_socket.settimeout(15.0)
            data = client_socket.recv(8192)
            req_str = data.decode('utf-8', errors='ignore')

            # --- ROUTING DE ATAQUE ---
            if "POST" in req_str or "PUT" in req_str or b"\x7fELF" in data:
                final_mode = "Malware Captured"
                sample = malware_triage.save_sample(data, ip)
                threading.Thread(target=malware_triage.perform_triage, args=(sample, os.getenv("VT_API_KEY")), daemon=True).start()
                zip_generator.serve_zip_trap(client_socket); return

            if "/tracking/beacon.png" in req_str: return

            if "GET /nomina" in req_str or "GET /conf" in req_str:
                final_mode = "Canary Served"
                canary_generator.serve_canary_file(client_socket, MY_PUBLIC_IP, f"NOMINA_{ip}.pdf"); return

            if local_port == 179: bgp_emulator.handle_bgp_open(client_socket, ip); return
            if local_port == 502: scada_emulator.scada_tarpit(client_socket); return
            
            if local_port in [445, 4455]:
                final_mode = "AD-Fake"
                total_bytes = smb_lethal.handle_smb_session(client_socket, ip)
            elif local_port == 22:
                final_mode = "SSH-Bait"
                shell_emulator.handle_cowrie_trap(client_socket, ip)
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
            if ip in self.stats:
                mb = round(total_bytes / (1024*1024), 4)
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
        try:
            network_mangler.apply_mss_clamping(PORTS)
            threading.Thread(target=icmp_tarpit.start_icmp_tarpit, args=({"127.0.0.1"},), daemon=True).start()
        except: pass
        for port in PORTS: threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        print(f"[🚀] {VERSION} IS LIVE. SYSTEM IS UNSTOPPABLE.")
        while True:
            try: time.sleep(1)
            except: break

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
