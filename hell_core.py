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

# CONFIGURACIÓN HELL v2.9.1-GOLD: FINAL SANITIZED VERSION
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [2222, 3389, 4455]
RAW_PORTS = [23, 445, 1433, 2323, 2525, 3306, 6379, 1337, 2375, 8125, 5060, 5900, 110, 5555]

PORTS = WEB_PORTS + LETHAL_PORTS + RAW_PORTS
GZIP_BOMB_PATH = "payloads/bomb.gz"
LOG_FILE = "logs/hell_activity.log"

VT_KEY = os.getenv("VT_API_KEY", "")
ISM_KEY = "b0959d3e-97c6-451f-9f95-5148c2da7ddd"
ISM_SECRET = "643a5731-1af4-4632-b75c-65955138288a"
MY_IP = os.getenv("MY_IP", "127.0.0.1")

ATTRACTIVE_PATHS = ["/.env", "/config", "/admin", "/setup", "/credentials", "/.git", "/backup"]
persistent_offenders = {}

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v2.9.1-GOLD: Final security audit complete. System initialized.")

    def get_country(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=country", timeout=3)
            return r.json().get('country', 'Unknown') if r.status_code == 200 else "Unknown"
        except: return "Unknown"

    def detect_scanner(self, data):
        data_str = data.decode('utf-8', errors='ignore')
        data_hex = binascii.hexlify(data).decode('utf-8')
        if "ff534d42" in data_hex: return "SMB/Windows Exploit Scanner"
        if "nmap" in data_str.lower(): return "Nmap Scripting Engine"
        if "masscan" in data_str.lower(): return "Masscan"
        if "zgrab" in data_str.lower(): return "ZGrab Scanner"
        if "shodan" in data_str.lower(): return "Shodan Bot"
        return "Unknown Bot / Scanner" if data else "TCP Stealth Scan"

    def log_event(self, ip, local_port, scanner, payload, duration=0, bytes_sent=0, status="START", intel=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        country = self.get_country(ip)
        if status == "START":
            log_entry = (
                f"\n[+] ATTACK INITIALIZED: {timestamp}\n"
                f"----------------------------------------\n"
                f"Origin Country: {country}\n"
                f"Attacker IP: {ip}\n"
                f"Target Port: {local_port}\n"
                f"Scanner Signature: {scanner}\n"
                f"Persistence: Hit #{persistent_offenders.get(ip, 1)}\n"
            )
        else:
            mb_sent = round(bytes_sent / (1024 * 1024), 2)
            log_entry = (
                f"[-] ATTACK CONCLUDED: {timestamp}\n"
                f"    └─ Persistence Duration: {round(duration, 2)}s\n"
                f"    └─ Data Absorbed: {mb_sent}MB\n"
                f"    └─ Mitigation Method: {status}\n"
                f"----------------------------------------\n"
            )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def clamped_send(self, client_socket, data):
        sent = 0
        try:
            for i in range(0, len(data), 2):
                chunk = data[i:i+2]
                client_socket.send(chunk)
                sent += len(chunk)
                time.sleep(random.uniform(0.01, 0.03))
        except: pass
        return sent

    def handle_web_request(self, client_socket, data, ip):
        try:
            request_str = data.decode('utf-8', errors='ignore')
            parts = request_str.split(' ')
            path = parts[1] if len(parts) > 1 else "/"
            
            # Sanitizar path para evitar inyección de headers o escape de assets
            path = os.path.basename(path) if "/" in path and not path.startswith("/") else path

            # TÉCNICA: Infinite Redirect Loop
            if "/trap/" in path or random.random() < 0.1:
                next_trap = f"/trap/{binascii.hexlify(os.urandom(4)).decode()}/"
                header = f"HTTP/1.1 302 Found\r\nLocation: {next_trap}\r\nContent-Length: 0\r\nConnection: keep-alive\r\n\r\n"
                client_socket.send(header.encode())
                return len(header)

            # TÉCNICA: Sticky Headers
            sticky = ""
            for i in range(50): sticky += f"X-Security-Audit-{i}: {binascii.hexlify(os.urandom(8)).decode()}\r\n"
            
            if any(p in path for p in ATTRACTIVE_PATHS):
                content = f"# HELL INTERNAL SECURITY SYSTEM\nIDENTIFIER={binascii.hexlify(os.urandom(16)).decode()}\n"
                header = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n{sticky}\r\n"
                return self.clamped_send(client_socket, (header + content).encode())

            # Carga de CPU Exhauster (WASM/JS)
            asset_path = "assets/cpu_heavy.js" if "cpu_heavy.js" in path else "assets/web_trap.html"
            mime = "application/javascript" if "js" in asset_path else "text/html"
            
            with open(asset_path, "rb") as f: content = f.read()
            header = f"HTTP/1.1 200 OK\r\nContent-Type: {mime}\r\n{sticky}\r\n"
            return self.clamped_send(client_socket, (header + content).encode())
        except Exception as e:
            print(f"Error handling web request: {e}")
            return 0

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        # Kernel-Level Keep-Alive Configuration
        try:
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            if hasattr(socket, "TCP_KEEPIDLE"):
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30)
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
        except: pass

        persistent_offenders[ip] = persistent_offenders.get(ip, 0) + 1
        start_time = time.time()
        total_bytes_sent = 0
        mode = "Sanitized Defense Interception"

        try:
            client_socket.settimeout(15.0)
            try: data = client_socket.recv(1024)
            except: data = b""

            scanner_type = self.detect_scanner(data)
            self.log_event(ip, local_port, scanner_type, data, status="START")

            if local_port in WEB_PORTS:
                mode = "Redirect Loop / CPU Exhauster"
                total_bytes_sent += self.handle_web_request(client_socket, data, ip)
                while True:
                    client_socket.send(os.urandom(1))
                    total_bytes_sent += 1
                    time.sleep(random.randint(15, 30))

            elif local_port in LETHAL_PORTS:
                mode = "L4 Zero-Window Tarpit"
                while True:
                    client_socket.send(os.urandom(1))
                    total_bytes_sent += 1
                    time.sleep(20)
            else:
                mode = "Infinite Data Stream"
                while True:
                    chunk = os.urandom(2048)
                    client_socket.send(chunk)
                    total_bytes_sent += len(chunk)
                    time.sleep(0.05)

        except: pass
        finally:
            duration = time.time() - start_time
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
