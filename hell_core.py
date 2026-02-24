import socket
import threading
import time
import os
import binascii
import random
import requests
from datetime import datetime
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter, IsMaliciousReporter

# CONFIGURACIÓN HELL v2.5.1: FULL FORENSIC LOGGING & IMPACT
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

persistent_offenders = {}

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"[💀] HELL CORE v2.5.1: Sistema de Log Forense Total ACTIVADO.")

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
        if data_hex.startswith("474554202f2048545450"): return "Generic HTTP Bot"
        return "Unknown Bot / Scanner" if data else "TCP Stealth Scan"

    def log_event(self, ip, local_port, scanner, payload, duration=0, bytes_sent=0, status="START", intel=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        country = self.get_country(ip)
        payload_hex = binascii.hexlify(payload[:32]).decode('utf-8') if payload else "None"
        
        if status == "START":
            intel_info = f"🔴 MALICIOUS (Score: {intel.get('score')})" if intel and intel.get('is_malicious') else "Checked"
            log_entry = (
                f"\n[+] ATTACK COMMENCED: {timestamp}\n"
                f"----------------------------------------\n"
                f"Origin Country: {country}\n"
                f"Attacker IP: {ip}\n"
                f"Target Port: {local_port}\n"
                f"Detected Activity: Active Scanner / Vulnerability Probing\n"
                f"Scanner Signature: {scanner}\n"
                f"Intel Status: {intel_info}\n"
                f"First Bytes Payload: {payload_hex}\n"
                f"Classification: Malicious Actor\n"
                f"Persistence: Hit #{persistent_offenders.get(ip, 1)}\n"
            )
        else:
            mb_sent = round(bytes_sent / (1024 * 1024), 2)
            log_entry = (
                f"[-] ATTACK NEUTRALIZED: {timestamp}\n"
                f"    └─ Duration: {round(duration, 2)} seconds\n"
                f"    └─ Data Injected: {mb_sent} MB\n"
                f"    └─ Termination: {status}\n"
                f"----------------------------------------\n"
            )
            
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)
        if status != "START":
            print(f"[⚔] {ip} ({country}) neutralizado tras {round(duration, 1)}s")

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        persistent_offenders[ip] = persistent_offenders.get(ip, 0) + 1
        start_time = time.time()
        total_bytes_sent = 0
        status = "Attacker Disconnected"

        try:
            client_socket.settimeout(4.0)
            try: payload = client_socket.recv(1024)
            except: payload = b""

            scanner_type = self.detect_scanner(payload)
            intel_result = self.ism_reporter.check_ip(ip)
            
            # Log de Inicio con todos los datos forenses solicitados
            self.log_event(ip, local_port, scanner_type, payload, status="START", intel=intel_result)
            
            if persistent_offenders[ip] % 10 == 1:
                self.vt_reporter.report_ip(ip, scanner=scanner_type, port=local_port, payload=payload)

            # --- ESTRATEGIAS DE CONTRAATAQUE ---
            
            if persistent_offenders[ip] > 5:
                while True:
                    client_socket.send(os.urandom(1))
                    total_bytes_sent += 1
                    time.sleep(random.randint(10, 30))

            elif "SMB" in scanner_type:
                fake_smb = binascii.unhexlify("0000002fff534d427200000000180120000000000000000000000000000005ff00000000")
                client_socket.send(fake_smb)
                total_bytes_sent += len(fake_smb)
                while True:
                    client_socket.send(os.urandom(1))
                    total_bytes_sent += 1
                    time.sleep(5)

            elif local_port in WEB_PORTS:
                if os.path.exists(GZIP_BOMB_PATH):
                    with open(GZIP_BOMB_PATH, "rb") as b: bomb_data = b.read()
                    header = f"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Length: {len(bomb_data)}\r\n\r\n"
                    client_socket.send(header.encode() + bomb_data)
                    total_bytes_sent += len(bomb_data)
                else:
                    msg = b"HTTP/1.1 200 OK\r\n\r\n<script>while(1)location.reload();</script>"
                    client_socket.send(msg)
                    total_bytes_sent += len(msg)
                time.sleep(5)

            else:
                chunk_size = 1024 if local_port in LETHAL_PORTS else 4096
                interval = 0.001 if local_port in LETHAL_PORTS else 0.1
                while True:
                    chunk = os.urandom(chunk_size)
                    client_socket.send(chunk)
                    total_bytes_sent += len(chunk)
                    time.sleep(interval)

        except (ConnectionResetError, BrokenPipeError):
            status = "Connection Reset (Attacker Fled)"
        except socket.timeout:
            status = "Socket Timeout"
        except Exception as e:
            status = f"Error: {str(e)}"
        finally:
            duration = time.time() - start_time
            self.log_event(ip, local_port, None, None, duration, total_bytes_sent, status)
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
