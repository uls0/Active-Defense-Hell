import os
import threading
import time
import socket
import sys
import json
import random
import requests
import signal
import psutil
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing, canary_generator, malware_triage, bgp_emulator, network_simulator, advanced_tarpit, threat_intel, abuse_api

VERSION = "v12.4-STORM"
LOG_FILE = "logs/hell_activity.log"
HOST = '0.0.0.0'
# Puertos expandidos para las 10 botnets
PORTS = [22, 23, 80, 443, 445, 88, 135, 139, 179, 389, 449, 502, 995, 1433, 2222, 2323, 3306, 3389, 4455, 8080, 8443, 9200, 33001, 1338, 8545, 3333, 18080, 32100, 14737]
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
        threading.Thread(target=zip_generator.precompute_bombs, daemon=True).start()
        self.stats = {}
        self.cpu_overload = False
        self.profiler = profiler_engine.HellProfiler()
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def check_system_health(self):
        while True:
            cpu_usage = psutil.cpu_percent(interval=5)
            self.cpu_overload = cpu_usage > 85
            time.sleep(10)

    def get_botnet_signature(self, port, ip):
        """Identifica botnets por puerto y comportamiento"""
        signatures = {
            23: "Mirai/Gafgyt (Telnet Botnet)",
            2323: "Mirai IoT Variant",
            14737: "Mozi P2P Node",
            32100: "QakBot C2 Beacon",
            995: "QakBot / Emotet Mail Stealer",
            449: "TrickBot Anchor",
            3333: "Mining Botnet (Stratum)",
            8545: "Aeternum C2 (Ethereum)",
            18080: "Aeternum C2 (Monero)",
            135: "REvil / Ransomware Recon",
            139: "REvil / Ransomware Recon"
        }
        return signatures.get(port, None)

    def get_full_intel(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp,proxy,reverse", timeout=1.2).json()
            return f"{r.get('city')}, {r.get('country')}", r.get('as', 'Unknown'), r.get('isp', 'Unknown'), r.get('reverse', ip), "PROXY/VPN" if r.get('proxy') else "RESIDENTIAL"
        except: return "Unknown", "Unknown", "Unknown", ip, "UNKNOWN"

    def log_engagement(self, ip, port, ja3=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        def background_log():
            loc, asn, isp, rdns, profile = self.get_full_intel(ip)
            botnet_name = self.get_botnet_signature(port, ip)
            
            if ip not in self.stats:
                intel = threat_intel.analyze_ip(ip, VT_KEY)
                self.stats[ip] = {'hits': 1, 'ports': [port], 'commands': [], 'ja3': ja3, 'total_time': 0, 'total_data': 0, 'loc': loc, 'asn': asn, 'isp': isp, 'rdns': rdns, 'profile': profile, 'intel': intel}
                
                # Reporte AUTOMATICO si detectamos una botnet conocida
                if botnet_name:
                    comment = f"HELL STORM DETECTION: Identified {botnet_name} node. Targeted port {port}. Origin: {loc}."
                    abuse_api.report_ip(ip, "14,15", comment)
                    threat_intel.report_ip_to_vt(ip, VT_KEY, comment)
            else:
                self.stats[ip]['hits'] += 1
                if port not in self.stats[ip]['ports']: self.stats[ip]['ports'].append(port)
            
            actor, conf = self.profiler.classify_attacker(self.stats[ip]['commands'], ja3, self.stats[ip]['ports'])
            
            prefix = f"[â˜¢ï¸ {botnet_name.upper()}]" if botnet_name else "[+] ULTIMATE DECEPTION TRIGGERED"
            report = f"\n{prefix}: {timestamp}\n----------------------------------------\nIP: {ip} ({rdns})\nOrigin: {loc} | Profile: {profile}\nNetwork: {isp} ({asn})\nClassification: {actor} ({conf}%)\nTarget Port: {port} | Hit Count: {self.stats[ip]['hits']}\n----------------------------------------\n"
            with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)
        threading.Thread(target=background_log, daemon=True).start()

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        start_time = time.time()
        self.log_engagement(ip, local_port)
        session_bytes = 0
        final_mode = "Mitigation"

        try:
            client_socket.settimeout(15.0)
            if local_port in [80, 443]:
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
                try:
                    with open("templates/miner.html", "r", encoding='utf-8') as f: response += f.read()
                except: response += "<html><body>Whatsminer S22 Admin</body></html>"
                client_socket.send(response.encode()); client_socket.close(); return

            data = client_socket.recv(8192)
            req_str = data.decode('utf-8', errors='ignore')
            if "POST" in req_str or "PUT" in req_str or b"\x7fELF" in data:
                final_mode = "Malware Captured"
                sample_path = malware_triage.save_sample(data, ip)
                threading.Thread(target=malware_triage.perform_triage, args=(sample_path, VT_KEY), daemon=True).start()
                zip_generator.serve_zip_trap(client_socket); return

            if local_port == 22:
                if self.cpu_overload:
                    advanced_tarpit.handle_advanced_tarpit(client_socket, ip, local_port)
                    final_mode = "CPU-Save-Tarpit"
                else:
                    shell_emulator.handle_cowrie_trap(client_socket, ip)
                    session_bytes = 42 * 1024 * 10; final_mode = "TITAN-Fifield-Burst"
                return

            if local_port in [445, 4455, 135, 139]:
                session_bytes = smb_lethal.handle_smb_session(client_socket, ip)
                final_mode = "HYDRA-GORGON-SMB"
                return

            # Tarpit mejorado para todo lo demas (incluyendo crypto y botnets)
            advanced_tarpit.handle_advanced_tarpit(client_socket, ip, local_port)
            final_mode = "Improved-Tarpit"
            return

        except: pass
        finally:
            session_duration = round(time.time() - start_time, 2)
            session_mb = round(session_bytes / (1024*1024), 4)
            closure_reason = "CLEAN_EXIT"
            try: client_socket.recv(1, socket.MSG_PEEK)
            except socket.timeout: closure_reason = "SILENT_DEATH (Timeout/Freeze)"
            except ConnectionResetError: closure_reason = "HOST_COLLAPSE (RST Received)"
            except: closure_reason = "GHOST_DISCONNECT"

            if ip in self.stats:
                self.stats[ip]['total_time'] += session_duration
                self.stats[ip]['total_data'] += session_mb
                actor, _ = self.profiler.classify_attacker(self.stats[ip]['commands'], None, self.stats[ip]['ports'])
                
                report = f"\n[-] THREAT NEUTRALIZED: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                report += f"    â””â”€ ATTACK TYPE: {actor} | MODE: {final_mode}\n"
                report += f"    â””â”€ SESSION DATA: {session_mb}MB | SESSION TIME: {session_duration}s\n"
                report += f"    â””â”€ TOTAL CUMULATIVE DAMAGE: Time Lost: {round(self.stats[ip]['total_time'], 2)}s | Data: {round(self.stats[ip]['total_data'], 2)}MB\n"
                report += f"    â””â”€ CLOSURE STATE: {closure_reason}\n"
                report += f"----------------------------------------\n"
                with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)
            client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port)); server.listen(500)
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except: pass

    def start(self):
        threading.Thread(target=self.check_system_health, daemon=True).start()
        for port in PORTS: threading.Thread(target=self.start_listener, args=(port,), daemon=True).start(); time.sleep(0.01)
        while True:
            try: time.sleep(1)
            except: break

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True); HellServer().start()
