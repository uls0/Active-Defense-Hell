import socket
import threading
import time
import os
import binascii
import random
import requests
import base64
import hashlib
import zlib
from datetime import datetime
from threat_intel import VirusTotalReporter, IsMaliciousReporter
from scripts import smb_lethal, shell_emulator, k8s_emulator

# CONFIGURACIÓN HELL v6.1.0: HONEY-KUBE & HIGH-VALUE SECRETS
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
K8S_PORTS = [6443, 8001] # API & Dashboard
RAW_PORTS = [21, 23, 25, 445, 1433, 2323, 2525, 3306, 6379, 1337, 2375, 8125, 5060, 5900, 110, 5555]
AD_PORTS = [53, 88, 135, 389, 636, 3268, 5985]
AI_PORTS = [11434, 8188, 1234, 3000]
VULN_PORTS = [10443]

PORTS = WEB_PORTS + LETHAL_PORTS + K8S_PORTS + RAW_PORTS + AD_PORTS + AI_PORTS + VULN_PORTS
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
        print(f"HELL CORE v6.1.0: Honey-Kube & High-Value Trap Paths active.")

    def log_event(self, ip, local_port, status="START", intel=None, duration=0):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if status == "START":
            log_entry = f"\n[+] DECEPTION TARGET TRIGGERED: {timestamp} | IP: {ip} | Port: {local_port}\n"
        else:
            log_entry = f"[-] TARGET RELEASED: {timestamp} | Held for: {round(duration, 2)}s | Mode: {status}\n"
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        start_time = time.time()
        self.log_event(ip, local_port, status="START")
        final_mode = "Retention"

        try:
            client_socket.settimeout(10.0)
            try: data = client_socket.recv(1024)
            except: data = b""
            
            req_str = data.decode('utf-8', errors='ignore')

            # --- PASO 2: HONEY-KUBE & SECRETS ---
            if local_port in K8S_PORTS or "/api/v1" in req_str:
                final_mode = "Honey-Kube Interaction"
                path = req_str.split(' ')[1] if ' ' in req_str else "/"
                
                if "/home/Desktop/backup_DB" in path:
                    k8s_emulator.serve_backup_trap(client_socket)
                    return

                resp = k8s_emulator.handle_k8s_request(path)
                header = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
                client_socket.send((header + json.dumps(resp)).encode())
                # Mantener conexión
                while True:
                    client_socket.send(b"\x00")
                    time.sleep(30)

            # --- PASO 1: DEEP SHELL ---
            elif local_port in [22, 2222]:
                final_mode = "Mainframe Shell Escape"
                shell_emulator.handle_mainframe_shell(client_socket, ip)
                return

            # --- OTROS ---
            elif local_port == 445:
                smb_lethal.handle_smb_attack(client_socket, ip, None, local_port)
                return

            else:
                while True:
                    client_socket.send(os.urandom(1024))
                    time.sleep(10)

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
