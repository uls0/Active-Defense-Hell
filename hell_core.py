import socket
import threading
import time
import os
import binascii
import random
import requests
import base64
import json
import zlib
import signal
import sys
from datetime import datetime
from threat_intel import VirusTotalReporter, IsMaliciousReporter
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler

# CONFIGURACIÓN HELL v8.0.0: RESOURCE EXHAUSTION (BURNOUT EDITION)
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
SCADA_PORTS = [502]
PORTS = WEB_PORTS + LETHAL_PORTS + SCADA_PORTS
LOG_FILE = "logs/hell_activity.log"

MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v8.0.0: Terminal Crusher & Fifield Bomb synchronized.")

    def log_event(self, ip, local_port, status="START", duration=0):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if status == "START":
            log_entry = f"\n[🔥] BURNOUT TARGET ENGAGED: {timestamp} | IP: {ip} | Port: {local_port}\n"
        else:
            log_entry = f"[-] EXHAUSTED: {timestamp} | Held: {round(duration, 2)}s | Mode: {status}\n"
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        start_time = time.time()
        self.log_event(ip, local_port, status="START")
        final_mode = "Mitigation"

        try:
            client_socket.settimeout(10.0)
            data = client_socket.recv(1024)
            req_str = data.decode('utf-8', errors='ignore')

            # --- WEB: FIFIELD BOMB & OWA ---
            if "/owa" in req_str or ".zip" in req_str or "GET / " in req_str:
                final_mode = "Fifield Ultra-Dense Attack"
                zip_generator.serve_zip_trap(client_socket)
                return

            # --- SSH: ANSI CRUSHER ---
            if local_port in [22, 2222]:
                final_mode = "Terminal Crusher (ANSI)"
                shell_emulator.handle_mainframe_shell(client_socket, ip)
                return

            # --- SCADA / RDP ---
            if local_port in SCADA_PORTS:
                final_mode = "SCADA Deception"
                scada_emulator.scada_tarpit(client_socket)
            elif local_port == 3389:
                final_mode = "RDP Bandwidth Murder"
                while True:
                    client_socket.send(os.urandom(1024 * 1024))
                    time.sleep(0.01)
            else:
                while True:
                    client_socket.send(b"\x00" * 1024)
                    time.sleep(15)

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
