import socket
import threading
import time
import os
import binascii
import random
import requests
import base64
import hashlib
from datetime import datetime
from threat_intel import VirusTotalReporter, IsMaliciousReporter
from scripts import smb_lethal

# CONFIGURACIÓN HELL v4.5.0: BEACON INJECTION & DEEP FORENSICS
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
RAW_PORTS = [21, 23, 25, 445, 1433, 2323, 2525, 3306, 6379, 1337, 2375, 8125, 5060, 5900, 110, 5555]
AD_PORTS = [53, 88, 135, 389, 636, 3268, 5985]
AI_PORTS = [11434, 8188, 1234, 3000]
VULN_PORTS = [10443]

PORTS = WEB_PORTS + LETHAL_PORTS + RAW_PORTS + AD_PORTS + AI_PORTS + VULN_PORTS
LOG_FILE = "logs/hell_activity.log"
GRABIFY_LINK = "https://grabify.link/MM6CBG"

VT_KEY = os.getenv("VT_API_KEY", "")
ISM_KEY = "b0959d3e-97c6-451f-9f95-5148c2da7ddd"
ISM_SECRET = "643a5731-1af4-4632-b75c-65955138288a"
MY_IP = os.getenv("MY_IP", "127.0.0.1")

ATTRACTIVE_PATHS = ["/.env", "/config", "/admin", "/setup", "/credentials", "/.git", "/backup", "/SYSVOL"]
persistent_offenders = {}

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v4.5.0: Beacon Tracking (Grabify) Active. Full forensics.")

    def get_deep_intel(self, ip):
        try:
            fields = "status,country,regionName,city,isp,as,proxy,hosting,query"
            r = requests.get(f"http://ip-api.com/json/{ip}?fields={fields}", timeout=3)
            if r.status_code == 200:
                d = r.json()
                profile = []
                if d.get('proxy'): profile.append("VPN/PROXY")
                if d.get('hosting'): profile.append("DATACENTER")
                return {
                    "location": f"{d.get('city')}, {d.get('regionName')}, {d.get('country')}",
                    "isp": f"{d.get('isp')} ({d.get('as')})",
                    "profile": " | ".join(profile) if profile else "RESIDENTIAL"
                }
        except: pass
        return {"location": "Unknown", "isp": "Unknown", "profile": "Unknown"}

    def log_event(self, ip, local_port, scanner, status="START", intel=None, duration=0, bytes_sent=0, payload=b""):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if status == "START":
            deep = self.get_deep_intel(ip)
            score = intel.get('score', 0) if intel else 0
            p_hash = hashlib.sha256(payload).hexdigest()[:16] if payload else "N/A"
            log_entry = (
                f"\n[+] DECEPTION ENGAGED: {timestamp}\n"
                f"----------------------------------------\n"
                f"IP: {ip} | Port: {local_port} | Profile: {deep['profile']}\n"
                f"Location: {deep['location']}\n"
                f"Network: {deep['isp']}\n"
                f"Intel: Score {score} | Signature: {scanner}\n"
                f"Attack Hash: {p_hash} | Beacon: Injected\n"
            )
        else:
            mb_sent = round(bytes_sent / (1024 * 1024), 4)
            log_entry = (
                f"[-] THREAT NEUTRALIZED: {timestamp}\n"
                f"    └─ Duration: {round(duration, 2)}s | Data: {mb_sent}MB\n"
                f"    └─ Method: {status}\n"
                f"----------------------------------------\n"
            )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def serve_honeytoken(self, client_socket, ip, path):
        """Sirve un archivo falso que incluye el Beacon de Grabify"""
        content = (
            f"# INTERNAL CONFIGURATION FILE\n"
            f"ADMIN_CREDENTIALS=admin:pass123\n"
            f"# EMERGENCY BEACON TRIGGER\n"
            f"REPORTING_SERVICE={GRABIFY_LINK}/telemetry.png\n"
            f"DEBUG_LOG_SERVER=http://{MY_IP}/internal/logs\n"
        )
        header = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n"
        client_socket.send(header.encode() + content.encode())
        return len(header) + len(content)

    def handle_web_request(self, client_socket, data, ip):
        try:
            request_str = data.decode('utf-8', errors='ignore')
            path = request_str.split(' ')[1] if ' ' in request_str else "/"
            
            if any(p in path for p in ATTRACTIVE_PATHS):
                return self.serve_honeytoken(client_socket, ip, path)

            if "cpu_heavy.js" in path:
                with open("assets/cpu_heavy.js", "rb") as f: content = f.read()
                mime = "application/javascript"
            else:
                with open("assets/web_trap.html", "rb") as f: content = f.read()
                mime = "text/html"
            
            header = f"HTTP/1.1 200 OK\r\nContent-Type: {mime}\r\nContent-Length: {len(content)}\r\n\r\n"
            client_socket.send(header.encode() + content)
            return len(header) + len(content)
        except: return 0

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        persistent_offenders[ip] = persistent_offenders.get(ip, 0) + 1
        start_time = time.time()
        total_bytes_sent = 0
        final_status = "Saturation Complete"

        try:
            client_socket.settimeout(10.0)
            try: data = client_socket.recv(1024, socket.MSG_PEEK)
            except: data = b""

            intel = self.ism_reporter.check_ip(ip)
            scanner = "Active Scanner"
            if b"GET" in data.upper(): scanner = "HTTP Bot"
            if b"SMB" in data: scanner = "SMB Bot"

            self.log_event(ip, local_port, scanner, status="START", intel=intel, payload=data)

            if local_port in [22, 2222]:
                final_status = "Infinite SSH Banner"
                # Inyectamos el link de Grabify en una línea del banner (algunos bots la siguen)
                client_socket.send(f"SSH-2.0-OpenSSH_8.9p1 (Audit-Info: {GRABIFY_LINK}/ssh)\r\n".encode())
                while True:
                    client_socket.send(f"ID-{random.randint(1000,9999)}: System Check OK\r\n".encode())
                    time.sleep(10)

            elif local_port == 445 or b"SMB" in data:
                final_status = "SMB Lethal Trap"
                total_bytes_sent = smb_lethal.handle_smb_attack(client_socket, ip, (lambda *args, **kwargs: None), local_port)
                return 

            elif local_port in WEB_PORTS or local_port in AI_PORTS:
                final_status = "Web Trap / Beacon"
                total_bytes_sent += self.handle_web_request(client_socket, data, ip)
                while True:
                    client_socket.send(os.urandom(1))
                    time.sleep(20)
            else:
                while True:
                    client_socket.send(os.urandom(65536))
                    total_bytes_sent += 65536
                    time.sleep(0.05)

        except: pass
        finally:
            duration = time.time() - start_time
            self.log_event(ip, local_port, None, status=final_status, duration=duration, bytes_sent=total_bytes_sent)
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
