import socket
import threading
import time
import os
import binascii
import random
import requests
import base64
import hashlib
import json
import zlib
import signal
import sys
from datetime import datetime
from threat_intel import VirusTotalReporter, IsMaliciousReporter
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, ja3_engine, icmp_tarpit, network_mangler, bgp_emulator, crypto_trap, canary_generator

# CONFIGURACIÓN HELL v7.2.0: DYNAMIC CANARYTOKENS & PDF TRACKING
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
K8S_PORTS = [6443, 8001]
SCADA_PORTS = [502]
ROUTING_PORTS = [179]
PORTS = WEB_PORTS + LETHAL_PORTS + K8S_PORTS + SCADA_PORTS + ROUTING_PORTS
LOG_FILE = "logs/hell_activity.log"

MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v7.2.0: Dynamic CanaryTokens (PDF Tracking) active.")

    def log_event(self, ip, local_port, status="START", duration=0, details=""):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if status == "START":
            log_entry = f"\n[+] DECEPTION TARGET: {timestamp} | IP: {ip} | Port: {local_port}\n"
        elif status == "CANARY_TRIGGER":
            log_entry = f"\n[🔔] CANARYTOKEN TRIGGERED: {timestamp} | IP REAL: {ip} | File: {details}\n"
        else:
            log_entry = f"[-] NEUTRALIZED: {timestamp} | Held for: {round(duration, 2)}s | Mode: {status}\n"
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        start_time = time.time()
        final_mode = "Mitigation"

        try:
            client_socket.settimeout(5.0)
            data = client_socket.recv(1024)
            req_str = data.decode('utf-8', errors='ignore')

            # --- PASO 7.2: CANARYTOKEN TRACKING ENDPOINT ---
            if "/tracking/beacon.png" in req_str:
                file_id = req_str.split('id=')[1].split(' ')[0] if 'id=' in req_str else "Unknown"
                self.log_event(ip, local_port, status="CANARY_TRIGGER", details=file_id)
                # Enviar pixel transparente
                pixel = binascii.unhexlify("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000a49444154789c63000100000500010d0a2db40000000049454e44ae426082")
                header = "HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n\r\n"
                client_socket.send(header.encode() + pixel)
                return

            # --- RUTA DE ARCHIVOS TENTADORES (Canary PDF) ---
            if ".pdf" in req_str or "NOMINA" in req_str or "ESTRATEGIA" in req_str:
                filename = "NOMINA_GRUPO_MODELO_2026.pdf"
                canary_generator.serve_canary_file(client_socket, MY_IP, filename)
                self.log_event(ip, local_port, status="START")
                return

            # --- OTROS MÓDULOS ---
            self.log_event(ip, local_port, status="START")
            if "wallet.dat" in req_str or "seed_phrase.txt" in req_str:
                final_mode = crypto_trap.serve_honey_wallet(client_socket, "wallet.dat")
            elif local_port == 179:
                bgp_emulator.handle_bgp_open(client_socket, ip)
            elif local_port in SCADA_PORTS:
                scada_emulator.scada_tarpit(client_socket)
            elif local_port in [22, 2222]:
                shell_emulator.handle_mainframe_shell(client_socket, ip)
            else:
                while True: client_socket.send(b"\x00"); time.sleep(30)

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
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        network_mangler.apply_mss_clamping(PORTS)
        threading.Thread(target=icmp_tarpit.start_icmp_tarpit, args=(self.whitelist,), daemon=True).start()
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    HellServer().start()
