import socket
import threading
import time
import os
import binascii
import random
import requests
import base64
from datetime import datetime
from threat_intel import VirusTotalReporter, IsMaliciousReporter
from scripts import smb_lethal

# CONFIGURACIÓN HELL v4.3.0: INFINITE SSH BANNERS & FULL PROTOCOL HOOKS
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

# BANNERS DE DECEPCIÓN PROFESIONAL
PROTOCOL_GREETINGS = {
    21: "220 (vsFTPd 3.0.5) - Nodo-Transferencia-Pemex-Logistica\r\n",
    22: "SSH-2.0-OpenSSH_8.9p1 (SISTEMAS-BANXICO-NODE-04)\r\n",
    2222: "SSH-2.0-OpenSSH_7.4p1-Service-Admin-SAT\r\n",
    23: "\r\nAcceso Restringido - Red Interna Telmex-Infinitum\r\nlogin: ",
    25: "220 mail.gob.mx ESMTP Postfix - Secretaria de Hacienda\r\n",
    110: "+OK POP3 Ready (Servidor de Correo Corporativo Soriana)\r\n",
    1433: "MSSQL Server 2019 - Node: MX-CORP-DATA-01\r\n",
    3306: binascii.unhexlify("4a0000000a352e372e33330008000000"),
    6379: "+OK\r\n",
    5900: "RFB 003.008\n",
    5060: "SIP/2.0 200 OK\r\nVia: SIP/2.0/UDP proxy.banorte.com.mx\r\n\r\n",
    2375: "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nServer: Docker/20.10.12 (Linux)\r\n\r\n",
    11434: "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nServer: Ollama/0.1.24\r\n\r\n",
}

persistent_offenders = {}

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v4.3.0: Infinite SSH Banners and Total Protocol Hooks deployed.")

    def get_intel_enriched(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,as,org", timeout=3)
            if r.status_code == 200:
                data = r.json()
                return data.get('country', 'Unknown'), data.get('as', 'Unknown ASN')
        except: pass
        return "Unknown", "Unknown ASN"

    def log_event(self, ip, local_port, scanner, status="START", intel=None, duration=0, bytes_sent=0):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if status == "START":
            country, asn = self.get_intel_enriched(ip)
            score = intel.get('score', 0) if intel else 0
            log_entry = (
                f"\n[+] DECEPTION ENGAGED: {timestamp}\n"
                f"----------------------------------------\n"
                f"Location: {country} | ISP: {asn}\n"
                f"Target: {local_port} | IP: {ip}\n"
                f"Intel Score: {score} | Signature: {scanner}\n"
            )
        else:
            mb_sent = round(bytes_sent / (1024 * 1024), 4)
            log_entry = (
                f"[-] THREAT NEUTRALIZED: {timestamp}\n"
                f"    └─ Persistence Duration: {round(duration, 2)}s\n"
                f"    └─ Data Injected: {mb_sent}MB\n"
                f"    └─ Final Strategy: {status}\n"
                f"----------------------------------------\n"
            )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def infinite_ssh_banner(self, client_socket, port):
        """Inyecta un banner infinito de líneas aleatorias para secuestrar el hilo del bot"""
        sent = 0
        banner = PROTOCOL_GREETINGS.get(port).encode()
        client_socket.send(banner)
        sent += len(banner)
        while True:
            # Enviamos falsos logs de sistema para mantener el interés del bot
            fake_log = f"ID-{random.randint(1000,9999)}: Internal System Check - Status OK...".encode()
            client_socket.send(fake_log + b"\r\n")
            sent += len(fake_log) + 2
            time.sleep(random.randint(5, 15))

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        persistent_offenders[ip] = persistent_offenders.get(ip, 0) + 1
        start_time = time.time()
        total_bytes_sent = 0
        final_status = "Saturation Complete"

        try:
            client_socket.settimeout(15.0)
            try: data = client_socket.recv(1024, socket.MSG_PEEK)
            except: data = b""

            intel = self.ism_reporter.check_ip(ip)
            self.log_event(ip, local_port, "Bot/Scanner", status="START", intel=intel)

            # --- FASE 1: INFINITE SSH TARPIT (22 & 2222) ---
            if local_port in [22, 2222]:
                final_status = "Infinite SSH Banner"
                total_bytes_sent = self.infinite_ssh_banner(client_socket, local_port)
                return

            # --- FASE 2: BANNERS REALISTAS PARA OTROS PUERTOS ---
            if local_port in PROTOCOL_GREETINGS:
                greet = PROTOCOL_GREETINGS[local_port]
                msg = greet if isinstance(greet, bytes) else greet.encode()
                client_socket.send(msg)
                total_bytes_sent += len(msg)

            # --- FASE 3: LETHAL CONTRAMEASURES ---
            if local_port == 445 or b"SMB" in data:
                final_status = "SMB Lethal Trap"
                total_bytes_sent = smb_lethal.handle_smb_attack(client_socket, ip, (lambda *args, **kwargs: None), local_port)
            elif local_port in LETHAL_PORTS: # 3389, 4455
                final_status = "L4 Zero-Window Tarpit"
                while True:
                    client_socket.send(os.urandom(1))
                    total_bytes_sent += 1
                    time.sleep(20)
            else:
                is_http = local_port in WEB_PORTS or local_port in AI_PORTS or b"GET" in data.upper()
                final_status = "Nested Math-Bomb" if is_http else "Saturation Flood"
                if is_http:
                    client_socket.send(b'{"system_integrity_check": [')
                    while True:
                        chunk = b'{"node":[' * 500
                        client_socket.send(chunk)
                        total_bytes_sent += len(chunk)
                        time.sleep(0.1)
                else:
                    while True:
                        chunk = os.urandom(65536)
                        client_socket.send(chunk)
                        total_bytes_sent += len(chunk)
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
