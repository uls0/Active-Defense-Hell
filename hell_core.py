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

VERSION = "v10.4.0-ULTIMATE-PURE"
LOG_FILE = "logs/hell_activity.log"
HOST = '0.0.0.0'
# Arsenal de Puertos Completo
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 179, 502, 8080, 8443, 9200, 4455]

class HellServer:
    def __init__(self):
        print(f"[*] INITIALIZING {VERSION}")
        os.makedirs("logs/forensics", exist_ok=True)
        os.makedirs("logs/malware", exist_ok=True)
        self.stats = {}
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def log_engagement(self, ip, port, ja3=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        def background_log():
            try:
                r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp", timeout=1.5).json()
                loc = f"{r.get('city')}, {r.get('country')}"
                asn = r.get('as')
            except: loc, asn = "Unknown", "Unknown"
            
            if ip not in self.stats: self.stats[ip] = {'hits': 1, 'ports': [port], 'commands': []}
            else: self.stats[ip]['hits'] += 1
            
            actor, conf = self.profiler.classify_attacker(self.stats[ip]['commands'], ja3, self.stats[ip]['ports'])
            report = f"\n[+] TRIGGERED: {timestamp} | IP: {ip} | Actor: {actor}({conf}%) | Port: {port} | Origin: {loc}\n"
            with open(LOG_FILE, "a") as f: f.write(report)
            print(f"[🔥] {actor} ENGAGED: {ip} on port {port}")
        
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
            
            # --- Ruteo de Emuladores Especializados ---
            if local_port == 179:
                bgp_emulator.handle_bgp_open(client_socket, ip)
                final_mode = "BGP-Deception"
                return
            
            if local_port == 502:
                scada_emulator.scada_tarpit(client_socket)
                final_mode = "SCADA-Tarpit"
                return

            if local_port == 8443:
                # Simular K8s API
                client_socket.send(b'{"kind": "Status", "status": "Failure", "message": "forbidden"}\n')
                final_mode = "K8s-Fake-API"
                return

            # --- Lógica Estándar ---
            if local_port in [445, 4455]:
                total_bytes = smb_lethal.handle_smb_session(client_socket, ip)
                final_mode = "AD-Labyrinth"
            elif local_port == 22:
                shell_emulator.handle_cowrie_trap(client_socket, ip)
                final_mode = "SSH-Bait"
            elif local_port == 3306:
                database_emulator.handle_mysql_trap(client_socket)
                final_mode = "MySQL-DataBomb"
            else:
                while True:
                    client_socket.send(b"\x00")
                    total_bytes += 1024; time.sleep(30)
        except: pass
        finally:
            duration = time.time() - start_time
            mb = round(total_bytes / (1024*1024), 4)
            with open(LOG_FILE, "a") as f:
                f.write(f"[-] NEUTRALIZED: {time.ctime()} | Held: {round(duration,2)}s | Data: {mb}MB | Mode: {final_mode}\n")
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
        # 1. Activación de Red (Protegida)
        try:
            network_mangler.apply_mss_clamping(PORTS)
            threading.Thread(target=icmp_tarpit.start_icmp_tarpit, args=({"127.0.0.1"},), daemon=True).start()
            print("[+] Network Layer defenses (ICMP/MSS) active.")
        except Exception as e: print(f"[⚠️] Network Layer error (Non-fatal): {e}")

        # 2. Activación de Listeners
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        
        print(f"[🚀] {VERSION} Deployment Complete. Ready for engagement.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
