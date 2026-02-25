import socket
import threading
import time
import os
import sys
import json
import random
import requests
import signal
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing, canary_generator, malware_triage, bgp_emulator, network_simulator, advanced_tarpit, threat_intel

VERSION = "v10.7.0-SINGULARITY-ELITE"
LOG_FILE = "logs/hell_activity.log"
HOST = '0.0.0.0'
# Puertos base + Rango Tarpit 20000-20100
PORTS = [22, 80, 443, 445, 88, 179, 389, 502, 1433, 2222, 3306, 3389, 4455, 8080, 8443, 9200, 33001, 1338]
PORTS.extend(range(20000, 20101))

MY_PUBLIC_IP = os.getenv("MY_IP", "127.0.0.1")
VT_KEY = os.getenv("VT_API_KEY", "")

class HellServer:
    def __init__(self):
        print(f"[*] INITIALIZING {VERSION} | TOTAL ARSENAL")
        os.makedirs("logs/forensics", exist_ok=True)
        os.makedirs("logs/malware", exist_ok=True)
        os.makedirs("logs/abuse_reports", exist_ok=True)
        os.makedirs("logs/intel_reports", exist_ok=True)
        self.stats = {}
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def get_full_intel(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp,proxy,reverse", timeout=1.2).json()
            loc = f"{r.get('city')}, {r.get('country')}"
            asn = r.get('as', 'Unknown')
            isp = r.get('isp', 'Unknown')
            rdns = r.get('reverse', ip)
            profile = "PROXY/VPN" if r.get('proxy') else "RESIDENTIAL"
            return loc, asn, isp, rdns, profile
        except: return "Unknown", "Unknown", "Unknown", ip, "UNKNOWN"

    def log_engagement(self, ip, port, ja3=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        def background_log():
            loc, asn, isp, rdns, profile = self.get_full_intel(ip)
            if ip not in self.stats:
                # Consulta VT solo para IPs nuevas
                intel = threat_intel.analyze_ip(ip, VT_KEY)
                self.stats[ip] = {
                    'hits': 1, 'ports': [port], 'commands': [], 'ja3': ja3, 
                    'total_time': 0, 'total_data': 0, 'loc': loc, 'asn': asn, 
                    'isp': isp, 'rdns': rdns, 'profile': profile, 'intel': intel
                }
            else:
                self.stats[ip]['hits'] += 1
                if port not in self.stats[ip]['ports']: self.stats[ip]['ports'].append(port)
            
            actor, conf = self.profiler.classify_attacker(self.stats[ip]['commands'], ja3, self.stats[ip]['ports'])
            
            report = f"\n[+] ULTIMATE DECEPTION TRIGGERED: {timestamp}\n"
            report += f"----------------------------------------\n"
            report += f"IP: {ip} ({rdns})\n"
            report += f"Origin: {loc} | Profile: {profile}\n"
            report += f"Network: {isp} ({asn})\n"
            report += f"Classification: {actor} ({conf}%)\n"
            report += f"Target Port: {port} | Hit Count: {self.stats[ip]['hits']}\n"
            report += f"----------------------------------------\n"
            
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
            data = client_socket.recv(8192)
            req_str = data.decode('utf-8', errors='ignore')

            # --- CAPTURA DE MALWARE ---
            if "POST" in req_str or "PUT" in req_str or b"\x7fELF" in data:
                final_mode = "Malware Captured"
                sample_path = malware_triage.save_sample(data, ip)
                threading.Thread(target=malware_triage.perform_triage, args=(sample_path, VT_KEY), daemon=True).start()
                zip_generator.serve_zip_trap(client_socket); return

            # --- ROUTING ---
            if "/tracking/beacon.png" in req_str: return
            if "GET /nomina" in req_str:
                canary_generator.serve_canary_file(client_socket, MY_PUBLIC_IP, f"NOMINA_{ip}.pdf")
                return

            if local_port == 22:
                shell_emulator.handle_cowrie_trap(client_socket, ip)
                total_bytes = 4 * 1024 * 1024; final_mode = "SSH-GigaBomb"
                return

            if local_port in [445, 4455]:
                total_bytes = smb_lethal.handle_smb_session(client_socket, ip)
                final_mode = "AD-Maze"
                return

            if 20000 <= local_port <= 20100:
                advanced_tarpit.handle_advanced_tarpit(client_socket, ip, local_port)
                final_mode = "Improved-Tarpit"
                return

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
                
                report = f"\n[-] THREAT NEUTRALIZED: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                report += f"    └─ TOTAL DAMAGE: Time Lost: {round(self.stats[ip]['total_time'], 2)}s | Data: {round(self.stats[ip]['total_data'], 2)}MB\n"
                report += f"----------------------------------------\n"
                
                with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)
                
                # --- DISPARADORES AUTOMÁTICOS ---
                if duration > 120 or mb > 5:
                    # Reporte de Abuso
                    threading.Thread(target=abuse_generator.generate_formal_report, args=(ip, self.stats[ip]['asn'], self.stats[ip]['loc'], None, duration, mb), daemon=True).start()
                    # Paquete Forense
                    threading.Thread(target=forensics_engine.create_evidence_pack, args=(ip, time.time()), daemon=True).start()
            client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(500)
            print(f"[✅] Port {port} armed.")
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except: pass

    def start(self):
        for port in PORTS: 
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
            time.sleep(0.01) # Pequeño delay para estabilizar el kernel
        print(f"[🚀] {VERSION} Deployment Complete.")
        while True:
            try: time.sleep(1)
            except: break

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
