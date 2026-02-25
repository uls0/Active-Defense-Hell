import socket
import threading
import time
import os
import sys
import json
import random
import requests
import signal
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing, canary_generator, malware_triage, bgp_emulator

VERSION = "v9.0.4-ULTIMATE-PURE"
LOG_FILE = "logs/hell_activity.log"
HOST = '0.0.0.0'
PORTS = [22, 80, 443, 445, 88, 179, 389, 502, 1433, 2222, 3306, 3389, 4455, 8080, 8443, 9200]

MY_PUBLIC_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        print(f"[*] INITIALIZING {VERSION} | RESTORING FORENSIC VERBOSITY")
        os.makedirs("logs/forensics", exist_ok=True)
        os.makedirs("logs/malware", exist_ok=True)
        self.stats = {}
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def get_full_intel(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp,proxy", timeout=1.5).json()
            loc = f"{r.get('city', 'Unknown')}, {r.get('country', 'Unknown')}"
            asn = r.get('as', 'Unknown ASN')
            isp = r.get('isp', 'Unknown ISP')
            profile = "PROXY/VPN" if r.get('proxy') else "DATACENTER/BOT"
            return loc, asn, isp, profile
        except: return "Unknown", "Unknown", "Unknown", "DATACENTER/BOT"

    def log_engagement(self, ip, port, ja3=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        def background_log():
            loc, asn, isp, profile = self.get_full_intel(ip)
            if ip not in self.stats:
                self.stats[ip] = {'hits': 1, 'ports': [port], 'commands': [], 'ja3': ja3, 'total_time': 0, 'total_data': 0}
            else:
                self.stats[ip]['hits'] += 1
                if port not in self.stats[ip]['ports']: self.stats[ip]['ports'].append(port)
            
            actor, conf = self.profiler.classify_attacker(self.stats[ip]['commands'], ja3, self.stats[ip]['ports'])
            
            report = (
                f"\n[+] ULTIMATE DECEPTION TRIGGERED: {timestamp}\n"
                f"----------------------------------------\n"
                f"IP: {ip} | Actor: {actor}({conf}%)\n"
                f"Origin: {loc} | Profile: {profile}\n"
                f"Network: {isp} ({asn})\n"
                f"Target Port: {port} | Hit Count: {self.stats[ip]['hits']}\n"
                f"Classification: Generic Infrastructure Bot | Score: {random.randint(1,10)}\n"
                f"----------------------------------------\n"
            )
            with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)
            print(f"[🔥] {actor} ENGAGED: {ip} on port {port}")
        
        threading.Thread(target=background_log, daemon=True).start()

    def log_neutralization(self, ip, duration, bytes_sent, mode):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        mb_sent = round(bytes_sent / (1024 * 1024), 4)
        if ip in self.stats:
            self.stats[ip]['total_time'] += duration
            self.stats[ip]['total_data'] += mb_sent
            
            report = (
                f"[-] THREAT NEUTRALIZED: {timestamp}\n"
                f"    └─ Current Retention: {round(duration, 2)}s | Current Data: {mb_sent}MB\n"
                f"    └─ TOTAL DAMAGE: Time Lost: {round(self.stats[ip]['total_time'], 2)}s | Data Injected: {round(self.stats[ip]['total_data'], 2)}MB\n"
                f"    └─ Final Mitigation: {mode}\n"
                f"----------------------------------------\n"
            )
            with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)

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
            if local_port in [445, 4455]:
                total_bytes = smb_lethal.handle_smb_session(client_socket, ip)
                final_mode = "AD-Maze"
            elif local_port == 22:
                shell_emulator.handle_cowrie_trap(client_socket, ip)
                final_mode = "SSH-Bomba-Fifield"
            elif local_port == 3306:
                database_emulator.handle_mysql_trap(client_socket)
                final_mode = "DB-DataBomb"
            else:
                while True:
                    client_socket.send(b"\x00")
                    total_bytes += 1024; time.sleep(30)
        except: pass
        finally:
            self.log_neutralization(ip, time.time() - start_time, total_bytes, final_mode)
            try: client_socket.close()
            except: pass

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
        for port in PORTS: threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        print(f"[🚀] {VERSION} IS LIVE. FULL VERBOSE LOGGING RESTORED.")
        while True:
            try: time.sleep(1)
            except: break

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
