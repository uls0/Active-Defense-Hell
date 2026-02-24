import socket
import threading
import time
import os
import binascii
import random
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter, IsMaliciousReporter

# CONFIGURACIÓN HELL v2.4.0: PERSISTENCE TRACKING & SMB TARPIT
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

# Rastreador de agresores
persistent_offenders = {} # {ip: count}

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"[💀] HELL CORE v2.4.0: Modo Tarpit Extremo para IPs persistentes ACTIVADO.")

    def detect_scanner(self, data):
        data_str = data.decode('utf-8', errors='ignore')
        data_hex = binascii.hexlify(data).decode('utf-8')
        
        if "ff534d42" in data_hex: return "SMB/Windows Exploit Scanner"
        if "nmap" in data_str.lower(): return "Nmap Scripting Engine"
        if "masscan" in data_str.lower(): return "Masscan"
        if "zgrab" in data_str.lower(): return "ZGrab Scanner"
        if "shodan" in data_str.lower(): return "Shodan Bot"
        if data_hex.startswith("474554202f2048545450"): return "Generic HTTP Bot"
        if data_hex.startswith("5353482d322e30"): return "SSH Brute-forcer"
        
        return "Unknown Bot / Scanner" if data else "TCP Stealth Scan"

    def log_event(self, ip, port, local_port, scanner, payload, intel_data=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        payload_preview = binascii.hexlify(payload[:32]).decode('utf-8') + "..." if payload else "None"
        hits = persistent_offenders.get(ip, 1)
        
        log_entry = (
            f"[{timestamp}] [HIT] {ip} -> Port:{local_port} (Hit #{hits})\n"
            f"    └─ Scanner: {scanner}\n"
            f"    └─ Payload: {payload_preview}\n"
        )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)
        print(f"[*] {scanner} ({ip}) detectado. Aplicando contramedidas...")

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        # Incrementar contador de agresor
        persistent_offenders[ip] = persistent_offenders.get(ip, 0) + 1
        is_repeat_offender = persistent_offenders[ip] > 5

        try:
            client_socket.settimeout(3.0)
            try: payload = client_socket.recv(1024)
            except: payload = b""

            scanner_type = self.detect_scanner(payload)
            self.log_event(ip, addr[1], local_port, scanner_type, payload)
            
            # Reportar solo si es nuevo o muy agresivo
            if persistent_offenders[ip] % 10 == 1:
                self.vt_reporter.report_ip(ip, scanner=scanner_type, port=local_port, payload=payload)

            # --- LÓGICA DE CONTRAATAQUE ---

            # CASO ESPECIAL: AGRESOR PERSISTENTE (MODO DEEP HELL)
            if is_repeat_offender:
                print(f"[🔥] IP {ip} es persistente. Entrando en DEEP HELL (Tarpit Extremo).")
                # Mantener la conexión abierta el mayor tiempo posible enviando datos ridículamente lento
                while True:
                    client_socket.send(os.urandom(1))
                    # Retraso aleatorio largo para frustrar timeouts automáticos
                    time.sleep(random.randint(10, 30)) 

            # CASO ESPECIAL: SMB TRAP (Port 4455 / SMB Signature)
            elif "SMB" in scanner_type:
                print(f"[🎣] SMB Trap activado para {ip}. Fingiendo negociación...")
                # Enviar un "Challenge" de SMB falso para que el bot espere más
                fake_smb_response = binascii.unhexlify("0000002f" + "ff534d42" + "7200000000180120000000000000000000000000000005ff00000000")
                client_socket.send(fake_smb_response)
                time.sleep(5)
                # Luego entrar en tarpit
                while True:
                    client_socket.send(os.urandom(1))
                    time.sleep(5)

            # RESPUESTAS ESTÁNDAR
            elif local_port in WEB_PORTS:
                if os.path.exists(GZIP_BOMB_PATH):
                    with open(GZIP_BOMB_PATH, "rb") as b: bomb_data = b.read()
                    header = f"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Length: {len(bomb_data)}\r\n\r\n"
                    client_socket.send(header.encode() + bomb_data)
                else:
                    client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n<script>while(1)location.reload();</script>")
            
            elif local_port in LETHAL_PORTS:
                # Fatiga TCP rápida
                while True:
                    client_socket.send(os.urandom(1024))
                    time.sleep(0.001)
            else:
                # Inundación estándar
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
