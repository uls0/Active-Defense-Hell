import socket
import threading
import time
import os
import binascii
import random
import requests
import base64
import hashlib
import zlib
from datetime import datetime
from threat_intel import VirusTotalReporter, IsMaliciousReporter
from scripts import smb_lethal, shell_emulator

# CONFIGURACIÓN HELL v6.0.0: DEEP SHELL EMULATION (Mainframe Edition)
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
RAW_PORTS = [21, 23, 25, 445, 1433, 2323, 2525, 3306, 6379, 1337, 2375, 8125, 5060, 5900, 110, 5555]
AD_PORTS = [53, 88, 135, 389, 636, 3268, 5985]
AI_PORTS = [11434, 8188, 1234, 3000]
VULN_PORTS = [10443]

PORTS = WEB_PORTS + LETHAL_PORTS + RAW_PORTS + AD_PORTS + AI_PORTS + VULN_PORTS
LOG_FILE = "logs/hell_activity.log"

VT_KEY = os.getenv("VT_API_KEY", "")
ISM_KEY = "b0959d3e-97c6-451f-9f95-5148c2da7ddd"
ISM_SECRET = "643a5731-1af4-4632-b75c-65955138288a"
MY_IP = os.getenv("MY_IP", "127.0.0.1")

damage_stats = {}

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v6.0.0: Deep Shell Emulation (Mainframe) Active.")

    def get_deep_intel(self, ip):
        location, isp, profile, rdns = "Unknown", "Unknown", "Unknown", "N/A"
        try: rdns = socket.gethostbyaddr(ip)[0]
        except: pass
        try:
            fields = "status,country,city,isp,as,proxy,hosting"
            r = requests.get(f"http://ip-api.com/json/{ip}?fields={fields}", timeout=3)
            if r.status_code == 200:
                d = r.json()
                location = f"{d.get('city')}, {d.get('country')}"
                isp = f"{d.get('isp')} ({d.get('as')})"
                profile = "DATACENTER" if d.get('hosting') else "RESIDENTIAL"
        except: pass
        return location, isp, profile, rdns

    def log_event(self, ip, local_port, status="START", intel=None, duration=0, bytes_sent=0):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if status == "START":
            loc, isp, prof, rdns = self.get_deep_intel(ip)
            log_entry = f"\n[+] DEEP SHELL TRIGGERED: {timestamp} | IP: {ip} | Port: {local_port} | Origin: {loc} | Network: {isp}\n"
        else:
            mb_sent = round(bytes_sent / (1024 * 1024), 2)
            log_entry = f"[-] ATTACKER NEUTRALIZED: {timestamp} | Duration: {round(duration, 2)}s | Total Impact: {mb_sent}MB | Mode: {status}\n"
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        start_time = time.time()
        self.log_event(ip, local_port, status="START")
        final_mode = "Standard Mitigation"

        try:
            # --- PASO 1: DEEP SHELL EMULATION (Port 22/2222) ---
            if local_port in [22, 2222]:
                final_mode = "Mainframe Shell Escape"
                shell_emulator.handle_mainframe_shell(client_socket, ip)
                return

            # --- RDP KILLBOX ---
            elif local_port == 3389:
                final_mode = "RDP Bandwidth Murder"
                while True:
                    client_socket.send(os.urandom(65536))
                    time.sleep(0.01)

            # --- SMB LETHAL ---
            elif local_port == 445:
                final_mode = "SMB Lethal Maze"
                smb_lethal.handle_smb_attack(client_socket, ip, None, local_port)
                return

            else:
                while True:
                    client_socket.send(os.urandom(1024))
                    time.sleep(5)

        except: pass
        finally:
            duration = time.time() - start_time
            self.log_event(ip, local_port, status=final_mode, duration=duration)
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
