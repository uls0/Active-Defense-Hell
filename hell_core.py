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
from datetime import datetime
from threat_intel import VirusTotalReporter, IsMaliciousReporter
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, ja3_engine

# CONFIGURACIÓN HELL v6.7.0: JA3 FINGERPRINTING & TLS PEERING
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
K8S_PORTS = [6443, 8001]
SCADA_PORTS = [502]
PORTS = WEB_PORTS + LETHAL_PORTS + K8S_PORTS + SCADA_PORTS
LOG_FILE = "logs/hell_activity.log"

VT_KEY = os.getenv("VT_API_KEY", "")
ISM_KEY = "b0959d3e-97c6-451f-9f95-5148c2da7ddd"
ISM_SECRET = "643a5731-1af4-4632-b75c-65955138288a"
MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v6.7.0: JA3 Fingerprinting Engine ready.")

    def log_event(self, ip, local_port, status="START", ja3=None, duration=0):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if status == "START":
            tool = ja3_engine.identify_client(ja3) if ja3 else "N/A"
            ja3_str = f" | JA3: {ja3} ({tool})" if ja3 else ""
            log_entry = f"\n[+] EVASION TARGET DETECTED: {timestamp} | IP: {ip} | Port: {local_port}{ja3_str}\n"
        else:
            log_entry = f"[-] NEUTRALIZED: {timestamp} | Time: {round(duration, 2)}s | Mode: {status}\n"
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        start_time = time.time()
        final_mode = "Mitigation"
        ja3_hash = None

        try:
            client_socket.settimeout(5.0)
            # Peek para JA3 si es un puerto TLS
            if local_port in [443, 8443, 6443]:
                initial_data = client_socket.recv(1024, socket.MSG_PEEK)
                ja3_hash = ja3_engine.get_ja3_hash(initial_data)

            self.log_event(ip, local_port, status="START", ja3=ja3_hash)

            # --- LÓGICA DE MÓDULOS ---
            data = client_socket.recv(1024)
            req_str = data.decode('utf-8', errors='ignore')

            if "/backup" in req_str or ".zip" in req_str:
                zip_generator.serve_zip_trap(client_socket)
                return

            if local_port in SCADA_PORTS:
                final_mode = "SCADA Deception"
                scada_emulator.scada_tarpit(client_socket)
            elif local_port in [22, 2222]:
                shell_emulator.handle_mainframe_shell(client_socket, ip)
            else:
                # Infinite Tarpit
                while True:
                    client_socket.send(b"\x00")
                    time.sleep(30)

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
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    HellServer().start()
