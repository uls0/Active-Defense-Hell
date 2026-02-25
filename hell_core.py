import socket
import threading
import time
import os
import sys
import requests
import signal
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing, canary_generator, malware_triage, network_simulator

VERSION = "v10.3.1-STABLE"
LOG_FILE = "logs/hell_activity.log"
HOST = '0.0.0.0'
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200, 4455]

class HellServer:
    def __init__(self):
        print(f"[*] INITIALIZING {VERSION}")
        os.makedirs("logs/forensics", exist_ok=True)
        self.stats = {}
        self.active_threads = 0
        try:
            self.ai = predictive_ai.HellPredictiveAI()
            self.profiler = profiler_engine.HellProfiler()
        except: pass
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def get_full_intel(self, ip):
        # Timeout agresivo para no bloquear el hilo de log
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp", timeout=1.5).json()
            return f"{r.get('city')}, {r.get('country')}", r.get('as'), r.get('isp')
        except: return "Unknown", "Unknown", "Unknown"

    def log_engagement(self, ip, port):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        # Corremos intel en un hilo para no retrasar el ataque
        def background_log():
            loc, asn, isp = self.get_full_intel(ip)
            if ip not in self.stats: self.stats[ip] = {'hits': 1, 'ports': [port], 'commands': []}
            else: self.stats[ip]['hits'] += 1
            actor, conf = self.profiler.classify_attacker(self.stats[ip]['commands'], None, self.stats[ip]['ports'])
            report = f"\n[+] TRIGGERED: {timestamp} | IP: {ip} | Actor: {actor}({conf}%) | Port: {port} | Origin: {loc}\n"
            with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)
            print(f"[🔥] {actor} ENGAGED: {ip} on {port}")
        
        threading.Thread(target=background_log, daemon=True).start()

    def handle_client(self, client_socket, addr, local_port):
        self.log_engagement(addr[0], local_port)
        start_time = time.time()
        total_bytes = 0
        try:
            client_socket.settimeout(15.0)
            if local_port in [445, 4455]:
                total_bytes = smb_lethal.handle_smb_session(client_socket, addr[0])
            elif local_port == 22:
                shell_emulator.handle_cowrie_trap(client_socket, addr[0])
            elif local_port == 3306:
                database_emulator.handle_mysql_trap(client_socket)
            else:
                while True:
                    client_socket.send(b"\x00")
                    total_bytes += 1024; time.sleep(30)
        except: pass
        finally:
            duration = time.time() - start_time
            mb = round(total_bytes / (1024*1024), 4)
            with open(LOG_FILE, "a") as f:
                f.write(f"[-] NEUTRALIZED: {time.ctime()} | Retention: {round(duration,2)}s | Data: {mb}MB\n")
            client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(500)
            print(f"[✅] Port {port}: ACTIVE")
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except Exception as e:
            print(f"[⚠️] Port {port} skipped: {e}")

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        print(f"[🚀] {VERSION} Deployment Complete.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
