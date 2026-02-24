import socket
import threading
import time
import os
import binascii
import random
import requests
import base64
from datetime import datetime
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter, IsMaliciousReporter
from scripts import smb_lethal

# CONFIGURACIÓN HELL v4.0.1-GOLD: INTEL SYNC & METRICS FIX
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
RAW_PORTS = [21, 23, 25, 445, 1433, 2323, 2525, 3306, 6379, 1337, 2375, 8125, 5060, 5900, 110, 5555]
AD_PORTS = [53, 88, 135, 389, 636, 3268, 5985]
AI_PORTS = [11434, 8188, 1234, 3000]
VULN_PORTS = [10443]

TOP_100_NMAP = [1, 3, 7, 9, 13, 17, 19, 21, 22, 23, 25, 26, 37, 53, 79, 80, 81, 88, 106, 110, 111, 113, 119, 135, 139, 143, 144, 179, 199, 389, 427, 443, 444, 445, 465, 513, 514, 515, 543, 544, 548, 554, 587, 631, 646, 873, 990, 993, 995, 1025, 1026, 1027, 1028, 1029, 1110, 1433, 1720, 1723, 1755, 1900, 2000, 2049, 2121, 2717, 3000, 3128, 3306, 3389, 3986, 4899, 5000, 5009, 5051, 5060, 5101, 5190, 5357, 5432, 5631, 5666, 5800, 5900, 6000, 6001, 6646, 7070, 8000, 8008, 8009, 8080, 8081, 8443, 8888, 9100, 9999, 10000]
SATURATION_PORTS = list(set(TOP_100_NMAP) - set(WEB_PORTS) - set(LETHAL_PORTS) - set(RAW_PORTS) - set(AD_PORTS) - set(AI_PORTS) - set(VULN_PORTS))
PORTS = WEB_PORTS + LETHAL_PORTS + RAW_PORTS + AD_PORTS + AI_PORTS + VULN_PORTS + SATURATION_PORTS

LOG_FILE = "logs/hell_activity.log"
VT_KEY = os.getenv("VT_API_KEY", "")
ISM_KEY = "b0959d3e-97c6-451f-9f95-5148c2da7ddd"
ISM_SECRET = "643a5731-1af4-4632-b75c-65955138288a"
MY_IP = os.getenv("MY_IP", "127.0.0.1")

persistent_offenders = {}
scan_sequences = {}

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v4.0.1-GOLD: Forensic Fixes applied. Monitoring {len(PORTS)} ports.")

    def get_country(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=country", timeout=3)
            return r.json().get('country', 'Unknown')
        except: return "Unknown"

    def log_event(self, ip, local_port, scanner, payload, duration=0, bytes_sent=0, status="START", intel=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        country = self.get_country(ip)
        if status == "START":
            # Restaurar Intel Status
            intel_info = "Unknown"
            if intel:
                score = intel.get('score', 0)
                is_mal = "MALICIOUS" if intel.get('is_malicious') else "Clean/Unknown"
                intel_info = f"{is_mal} (Score: {score})"
            
            log_entry = (
                f"\n[+] ENTERPRISE DECEPTION TRIGGERED: {timestamp}\n"
                f"----------------------------------------\n"
                f"Origin Country: {country}\n"
                f"Attacker IP: {ip}\n"
                f"Target Port: {local_port}\n"
                f"Scanner Signature: {scanner}\n"
                f"Intel Status: {intel_info}\n"
                f"Persistence: Hit #{persistent_offenders.get(ip, 1)}\n"
            )
        else:
            mb_sent = round(bytes_sent / (1024 * 1024), 2)
            log_entry = (
                f"[-] THREAT NEUTRALIZED: {timestamp}\n"
                f"    └─ Persistence Duration: {round(duration, 2)}s\n"
                f"    └─ Data Injected: {mb_sent}MB\n"
                f"    └─ Mitigation Method: {status}\n"
                f"----------------------------------------\n"
            )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        persistent_offenders[ip] = persistent_offenders.get(ip, 0) + 1
        start_time = time.time()
        total_bytes_sent = 0
        mode = "Generic Deception"

        try:
            client_socket.settimeout(15.0)
            try: data = client_socket.recv(1024, socket.MSG_PEEK)
            except: data = b""

            # Consultar Inteligencia
            intel_result = self.ism_reporter.check_ip(ip)
            scanner_type = "Active Scanner" # Simplificado para el log
            
            self.log_event(ip, local_port, scanner_type, data, status="START", intel=intel_result)
            
            # Reportar a VirusTotal (confirmación en consola)
            if persistent_offenders[ip] % 5 == 1:
                self.vt_reporter.report_ip(ip, scanner=scanner_type, port=local_port, payload=data)

            # --- ESTRATEGIAS ---
            if local_port == 445 or b"SMB" in data:
                mode = "SMB Lethal Trap"
                smb_lethal.handle_smb_attack(client_socket, ip, self.log_event, local_port)
                # Nota: smb_lethal maneja su propio bucle
                return 

            elif local_port in LETHAL_PORTS:
                mode = "L4 Tarpit"
                while True:
                    client_socket.send(os.urandom(1))
                    total_bytes_sent += 1
                    time.sleep(20)
            else:
                mode = "Data Flood"
                while True:
                    chunk = os.urandom(2048)
                    client_socket.send(chunk)
                    total_bytes_sent += len(chunk)
                    time.sleep(0.1)

        except: pass
        finally:
            duration = time.time() - start_time
            if mode != "SMB Lethal Trap": # SMB ya loguea su fin
                self.log_event(ip, local_port, None, None, duration, total_bytes_sent, mode)
            try: client_socket.close()
            except: pass

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(100)
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except: pass

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    HellServer().start()
