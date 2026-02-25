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
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator

# CONFIGURACIÓN HELL v6.4.0: BROWSER HOOKING & HEADLESS CRUSHER
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
        print(f"HELL CORE v6.4.0: Browser Hooking Active (Headless Detection enabled).")

    def log_event(self, ip, local_port, status="START", intel=None, duration=0):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if status == "START":
            log_entry = f"\n[+] WEB TARGET ENGAGED: {timestamp} | IP: {ip} | Port: {local_port}\n"
        else:
            log_entry = f"[-] NEUTRALIZED: {timestamp} | Time: {round(duration, 2)}s | Mode: {status}\n"
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def handle_web_request(self, client_socket, ip, req_str):
        """Maneja peticiones HTTP inyectando trampas y hooks"""
        # Servir el script de Hooking
        if "GET /js/hook.js" in req_str:
            with open("assets/hook.js", "r", encoding='utf-8') as f:
                content = f.read()
            header = "HTTP/1.1 200 OK\r\nContent-Type: application/javascript\r\n\r\n"
            client_socket.send((header + content).encode())
            return "Browser Hook Sent"

        # Servir OWA Grupo Modelo
        if "/owa" in req_str or "/exchange" in req_str or "/microsoft" in req_str or "GET / " in req_str:
            with open("assets/owa_modelo.html", "r", encoding='utf-8') as f:
                content = f.read()
            header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            client_socket.send((header + content).encode())
            return "OWA Deception Served"

        return "Generic Web Tarpit"

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        start_time = time.time()
        self.log_event(ip, local_port, status="START")
        final_mode = "Retention"

        try:
            client_socket.settimeout(10.0)
            data = client_socket.recv(1024)
            req_str = data.decode('utf-8', errors='ignore')

            # --- WEB PORTS ---
            if local_port in WEB_PORTS:
                final_mode = self.handle_web_request(client_socket, ip, req_str)
                if "Deception" in final_mode or "Hook" in final_mode:
                    # Mantener conexión viva para que el script corra
                    while True:
                        client_socket.send(b"\x00")
                        time.sleep(20)

            # --- OTROS MODULOS ---
            elif local_port in SCADA_PORTS:
                final_mode = "SCADA Deception"
                scada_emulator.scada_tarpit(client_socket)
            elif local_port in K8S_PORTS:
                final_mode = "Honey-Kube"
                client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")
                while True: client_socket.send(b"\x00"); time.sleep(30)
            elif local_port in [22, 2222]:
                final_mode = "Mainframe Shell"
                shell_emulator.handle_mainframe_shell(client_socket, ip)
            else:
                while True: client_socket.send(os.urandom(1024)); time.sleep(10)

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
