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

# CONFIGURACIÓN HELL v4.0.0: ENTERPRISE DECEPTION & AI THEFT TRAPS
HOST = '0.0.0.0'

# Puertos Especializados
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
RAW_PORTS = [21, 23, 25, 445, 1433, 2323, 2525, 3306, 6379, 1337, 2375, 8125, 5060, 5900, 110, 5555]

# MÓDULO 1: Active Directory (MEX-AD-CORP)
AD_PORTS = [53, 88, 135, 389, 636, 3268, 5985]

# MÓDULO 2: Inteligencia Artificial (Agotamiento de Mineros/Ladrones de Modelos)
AI_PORTS = [11434, 8188, 1234, 3000]

# MÓDULO 3: Vulnerabilidades Críticas 2026 (Fortinet, Roundcube)
VULN_PORTS = [10443]

# Generar lista de saturación (Top 100 Nmap saltando los ya usados)
TOP_100_NMAP = [1, 3, 7, 9, 13, 17, 19, 21, 22, 23, 25, 26, 37, 53, 79, 80, 81, 88, 106, 110, 111, 113, 119, 135, 139, 143, 144, 179, 199, 389, 427, 443, 444, 445, 465, 513, 514, 515, 543, 544, 548, 554, 587, 631, 646, 873, 990, 993, 995, 1025, 1026, 1027, 1028, 1029, 1110, 1433, 1720, 1723, 1755, 1900, 2000, 2049, 2121, 2717, 3000, 3128, 3306, 3389, 3986, 4899, 5000, 5009, 5051, 5060, 5101, 5190, 5357, 5432, 5631, 5666, 5800, 5900, 6000, 6001, 6646, 7070, 8000, 8008, 8009, 8080, 8081, 8443, 8888, 9100, 9999, 10000, 32768, 49152, 49153, 49154, 49155, 49156, 49157]
SATURATION_PORTS = list(set(TOP_100_NMAP) - set(WEB_PORTS) - set(LETHAL_PORTS) - set(RAW_PORTS) - set(AD_PORTS) - set(AI_PORTS) - set(VULN_PORTS))

PORTS = WEB_PORTS + LETHAL_PORTS + RAW_PORTS + AD_PORTS + AI_PORTS + VULN_PORTS + SATURATION_PORTS

GZIP_BOMB_PATH = "payloads/bomb.gz"
LOG_FILE = "logs/hell_activity.log"

VT_KEY = os.getenv("VT_API_KEY", "")
ISM_KEY = "b0959d3e-97c6-451f-9f95-5148c2da7ddd"
ISM_SECRET = "643a5731-1af4-4632-b75c-65955138288a"
MY_IP = os.getenv("MY_IP", "127.0.0.1")

ATTRACTIVE_PATHS = [
    "/.env", "/config", "/admin", "/setup", "/credentials", "/.git", "/backup",
    "/SYSVOL", "/NETLOGON", "/Policies", "/Groups.xml", "/Policies.ini", # AD Honeytokens
    "/v1/models", "/api/chat", "/prompt" # AI Honeytokens
]

persistent_offenders = {}
scan_sequences = {}

MEXICAN_BANNERS = {
    21: "220 (vsFTPd 3.0.5) - Nodo-Transferencia-Pemex-Logistica\r\n",
    22: "SSH-2.0-OpenSSH_8.9p1 (SISTEMAS-BANXICO-NODE-04)\r\n",
    23: "\r\nAcceso Restringido - Red Interna Telmex-Infinitum\r\nlogin: ",
    25: "220 mail.gob.mx ESMTP Postfix - Secretaria de Hacienda\r\n",
    110: "+OK POP3 Ready (Servidor de Correo Corporativo Soriana)\r\n",
    1433: "MSSQL Server 2019 - Node: MX-CORP-DATA-01\r\n",
    3306: "5.7.33-0ubuntu0.18.04.1 (MySQL-Server-Bimbo-Produccion)\r\n"
}

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v4.0.0: ENTERPRISE DECEPTION. Vigilando {len(PORTS)} puertos (AD, AI, SATURATION).")

    def track_scan(self, ip, port):
        if ip not in scan_sequences: scan_sequences[ip] = []
        scan_sequences[ip].append(port)
        if len(scan_sequences[ip]) > 3:
            seq = scan_sequences[ip][-3:]
            if abs(seq[0] - seq[1]) <= 2 and abs(seq[1] - seq[2]) <= 2:
                return True
        return False

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
                f"\n[+] ENTERPRISE DECEPTION TRIGGERED: {timestamp}\n"
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
                f"[-] THREAT NEUTRALIZED: {timestamp}\n"
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

    def generate_fake_fortinet_login(self, client_socket):
        """Simula una página de login de FortiGate vulnerable"""
        html = "<html><head><title>FortiGate Login</title></head><body><h1>FortiOS 7.0 - VPN Gateway</h1><form action='/logincheck' method='POST'><input name='username'/><input type='password' name='secretkey'/></form></body></html>"
        header = f"HTTP/1.1 200 OK\r\nServer: FortiGate\r\nContent-Type: text/html\r\n\r\n"
        return self.clamped_send(client_socket, (header + html).encode())

    def handle_web_request(self, client_socket, data, ip, local_port):
        try:
            request_str = data.decode('utf-8', errors='ignore')
            parts = request_str.split(' ')
            path = parts[1] if len(parts) > 1 else "/"
            
            # 1. Fortinet / Roundcube Deception
            if local_port in VULN_PORTS or local_port in [80, 443]:
                if "/login" in path or "/remote/login" in path or local_port == 10443:
                    return self.generate_fake_fortinet_login(client_socket)
            
            # 2. Infinite Redirect Loop
            if "/trap/" in path or random.random() < 0.1:
                next_trap = f"/trap/{binascii.hexlify(os.urandom(4)).decode()}/"
                header = f"HTTP/1.1 302 Found\r\nLocation: {next_trap}\r\nContent-Length: 0\r\nConnection: keep-alive\r\n\r\n"
                client_socket.send(header.encode())
                return len(header)

            # 3. Sticky Headers + Honeytokens (AD / AI)
            sticky = ""
            for i in range(50): sticky += f"X-Security-Audit-{i}: {binascii.hexlify(os.urandom(8)).decode()}\r\n"
            
            if any(p in path for p in ATTRACTIVE_PATHS):
                content = f"# DOMAIN CONTROLLER SECRETS OR AI MODEL METADATA\nACCESS_TOKEN={binascii.hexlify(os.urandom(16)).decode()}\n"
                header = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n{sticky}\r\n"
                return self.clamped_send(client_socket, (header + content).encode())

            # 4. CPU Exhauster (WASM/JS)
            asset_path = "assets/cpu_heavy.js" if "cpu_heavy.js" in path else "assets/web_trap.html"
            mime = "application/javascript" if "js" in asset_path else "text/html"
            
            with open(asset_path, "rb") as f: content = f.read()
            header = f"HTTP/1.1 200 OK\r\nContent-Type: {mime}\r\n{sticky}\r\n"
            return self.clamped_send(client_socket, (header + content).encode())
        except Exception:
            return 0

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        try:
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            if hasattr(socket, "TCP_KEEPIDLE"):
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30)
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
        except: pass

        persistent_offenders[ip] = persistent_offenders.get(ip, 0) + 1
        is_hopping = self.track_scan(ip, local_port)
        start_time = time.time()
        total_bytes_sent = 0
        mode = "Sanitized Defense Interception"

        try:
            client_socket.settimeout(15.0)
            
            # --- FASE 1: BANNERS DE ENGANHO CORPORATIVO ---
            if local_port in MEXICAN_BANNERS:
                client_socket.send(MEXICAN_BANNERS[local_port].encode())
                
            try: data = client_socket.recv(1024)
            except: data = b""

            scanner_type = self.detect_scanner(data)
            self.log_event(ip, local_port, scanner_type, data, status="START")

            # --- FASE 2: CONTRAMEDIDAS LETHALES ---

            # A. KILLSWITCH (Port-Hopping)
            if is_hopping:
                mode = "Port-Hopping Killswitch"
                client_socket.send(os.urandom(1024) + b"\x00\xff\x00\xff")
                time.sleep(1)
                return

            # B. SMB ADVANCED COUNTER-ATTACKS (Puerto 445 / 139)
            elif local_port == 445 or b"SMB" in data:
                mode = "SMB Active Defense"
                smb_lethal.handle_smb_attack(client_socket, ip, self.log_event, local_port)
                return

            # C. AI THIEF TRAPS (ComfyUI, Ollama, LM Studio)
            elif local_port in AI_PORTS:
                mode = "AI Model Thief Trap"
                if local_port == 11434: # Ollama fake response
                    client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n{\"models\": [{\"name\": \"llama3:8b-instruct-q4_K_M\", \"size\": 4700000000}]}")
                else: # Generic JSON Trap
                    client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n{\"status\": \"loading_weights\", \"progress\": 0.01}")
                # Entrar en Drip-feed
                while True:
                    client_socket.send(b"\x00")
                    total_bytes_sent += 1
                    time.sleep(10)

            # D. ACTIVE DIRECTORY DECEPTION
            elif local_port in AD_PORTS:
                mode = "Active Directory Deception Loop"
                while True:
                    client_socket.send(os.urandom(16)) # Basura que confunde parsers LDAP/Kerberos
                    total_bytes_sent += 16
                    time.sleep(5)

            # E. WEB & VULN TRAPS (Fortinet, Roundcube, CPU Exhauster)
            elif local_port in WEB_PORTS or local_port in VULN_PORTS:
                mode = "Web Decoy / Redirect / CPU Exhauster"
                total_bytes_sent += self.handle_web_request(client_socket, data, ip, local_port)
                while True:
                    client_socket.send(os.urandom(1))
                    total_bytes_sent += 1
                    time.sleep(random.randint(15, 30))

            # F. LETHAL TARPIT (Port 22, 3389, etc)
            elif local_port in LETHAL_PORTS:
                mode = "L4 Zero-Window Tarpit"
                while True:
                    client_socket.send(os.urandom(1))
                    total_bytes_sent += 1
                    time.sleep(20)

            # G. SATURATION FLOOD (Top 100 Nmap)
            else:
                mode = "Saturation Data Flood"
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
