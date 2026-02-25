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
from threat_intel import VirusTotalReporter, AbuseIPDBReporter, IsMaliciousReporter

# CONFIGURACIÓN HELL v9.6.0: EXTERNAL INTEL SYNC
HOST = '0.0.0.0'
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200, 4455]
LOG_FILE = "logs/hell_activity.log"

# API KEYS (Cargadas desde entorno para seguridad)
VT_KEY = os.getenv("VT_API_KEY", "")
ABUSE_KEY = os.getenv("ABUSE_API_KEY", "")
ISMAL_KEY = os.getenv("ISMAL_API_KEY", "")

class HellServer:
    def __init__(self):
        os.makedirs("logs/forensics", exist_ok=True)
        self.stats = {} # {ip: {'hits': X, 'reported': False, ...}}
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        
        # Inicializar reporteros externos
        self.vt = VirusTotalReporter(VT_KEY)
        self.abuse_db = AbuseIPDBReporter(ABUSE_KEY)
        self.ismal = IsMaliciousReporter(ISMAL_KEY, "")

        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()
        print("Designed by ULSO+GCLI | HELL CORE v9.6.0 Operational.")

    def async_report(self, ip, port, actor, loc, isp):
        """Envía reportes a inteligencias globales cada 5 hits"""
        print(f"[*] Analyzing IP {ip} for global reporting...")
        self.vt.report_ip(ip, scanner=actor, port=port, location=loc, isp=isp)
        self.abuse_db.report_ip(ip, port, comment=f"Adversary Profile: {actor} detected by HELL Core.")

    def log_engagement(self, ip, port, ja3=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        loc, asn, isp = self.get_full_intel(ip)
        
        if ip not in self.stats:
            self.stats[ip] = {'hits': 1, 'ports': [port], 'commands': [], 'ja3': ja3, 'reported': False}
        else:
            self.stats[ip]['hits'] += 1
            if port not in self.stats[ip]['ports']: self.stats[ip]['ports'].append(port)

        actor, conf = self.profiler.classify_attacker(self.stats[ip]['commands'], ja3, self.stats[ip]['ports'])
        
        # REGLA: Reportar cada 5 hits
        if self.stats[ip]['hits'] % 5 == 0:
            threading.Thread(target=self.async_report, args=(ip, port, actor, loc, isp), daemon=True).start()

        report = (
            f"\n[+] ULTIMATE DECEPTION TRIGGERED: {timestamp}\n"
            f"----------------------------------------\n"
            f"IP: {ip} | Actor: {actor} ({conf}%)\n"
            f"Origin: {loc} | Network: {isp}\n"
            f"Target Port: {port} | Session Hits: {self.stats[ip]['hits']}\n"
            f"Status: MONITORING & REPORTING ACTIVE\n"
            f"----------------------------------------\n"
        )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)
        print(f"[*] {actor} Engaged: {ip}:{port}")

    def get_full_intel(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp", timeout=3).json()
            return f"{r.get('city')}, {r.get('country')}", r.get('as'), r.get('isp')
        except: return "Unknown", "Unknown", "Unknown"

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        self.log_engagement(ip, local_port)
        try:
            client_socket.settimeout(10.0)
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
            server.listen(300)
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except: time.sleep(10)

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        print("[✅] HELL v9.6.0: Intel Sync Active.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
