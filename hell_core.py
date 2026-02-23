import socket
import threading
import time
import random
import os
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter

# CONFIGURACIÓN HELL v1.6.0: ENTERPRISE DECEPTION
HOST = '0.0.0.0'
# Puertos: 8080(Web), 2525(SMTP), 3306(MySQL), 2222(SSH), 3389(RDP), 6379(Redis), 4455(SMB), 1337(Switch)
# NUEVOS ENTERPRISE: 2375(Docker), 8090(Jira), 8125(Datadog), 8443(Ansible/Snyk)
PORTS = [8080, 2525, 3306, 2222, 3389, 6379, 4455, 1337, 8081, 2375, 8090, 8125, 8443]
GZIP_BOMB_PATH = "payloads/bomb.gz"
LOG_FILE = "logs/hell_activity.log"

USE_AI = os.getenv("USE_AI", "false").lower() == "true"
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
VT_KEY = os.getenv("VT_API_KEY", "")
MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        self.defender = GeminiDefender(GEMINI_KEY) if USE_AI else None
        self.reporter = VirusTotalReporter(VT_KEY)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"[💀] HELL CORE v1.6.0: ENTERPRISE DECEPTION - LETHAL MODE")

    def log_event(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(message)

    def send_response(self, client_socket, content, content_type="text/html", status="200 OK"):
        header = f"HTTP/1.1 {status}\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n"
        client_socket.send(header.encode() + content.encode())

    def linux_fatigue_stream(self, client_socket):
        """Genera fatiga extrema de CPU/Kernel mediante interrupciones masivas"""
        try:
            while True:
                client_socket.send(os.urandom(1)) # 1 byte para saturar el stack de red
                time.sleep(0.001)
        except: pass

    def handle_jenkins_cerberus(self, client_socket, addr, request):
        """Jenkins Trap con Cerberus Ph 2: Honey-tokens"""
        if "GET /credentials" in request:
            self.log_event(f"[🕵️] Cerberus Ph 2: Atacante {addr[0]} descargando Honey-tokens de AWS.")
            keys = '{"access_key": "AKIAUI7EXAMPLE", "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLE"}'
            self.send_response(client_socket, keys, content_type="application/json")
            self.reporter.report_ip(addr[0])
        else:
            content = "<h1>Jenkins Dashboard</h1><a href='/credentials'>Manage Credentials</a>"
            self.send_response(client_socket, content)

    def handle_docker_api(self, client_socket, addr):
        """Docker Engine API Trap: Infinite JSON Junk"""
        self.log_event(f"[🐳] Docker API Scan detectado desde {addr[0]}")
        client_socket.send(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nTransfer-Encoding: chunked\r\n\r\n")
        try:
            while True:
                chunk = b'[{"Id":"' + os.urandom(32).hex().encode() + b'","Names":["/fake_container_prod"]},{"Status":"Running"}]'
                size = hex(len(chunk))[2:]
                client_socket.send(f"{size}\r\n".encode() + chunk + b"\r\n")
                time.sleep(0.1)
        except: pass

    def handle_client(self, client_socket, addr, local_port):
        if addr[0] in self.whitelist:
            client_socket.close(); return

        try:
            # Peticiones de alto valor (Docker, Jira, Ansible)
            if local_port == 2375: self.handle_docker_api(client_socket, addr)
            elif local_port == 8081: 
                request = client_socket.recv(1024).decode('utf-8', errors='ignore')
                self.handle_jenkins_cerberus(client_socket, addr, request)
            elif local_port in [8090, 8125, 8443]: # Jira, Datadog, Ansible/Snyk
                self.log_event(f"[⚡] Enterprise App hit en puerto {local_port} desde {addr[0]}")
                # Iniciar fatiga de Kernel inmediata
                self.linux_fatigue_stream(client_socket)
            elif local_port == 1337: # El portal del Switch/C2 (fijo)
                request = client_socket.recv(1024).decode('utf-8', errors='ignore')
                # (Lógica previa de trap_1337.html)
                self.linux_fatigue_stream(client_socket)
            else:
                # Otros puertos: Basura binaria
                self.linux_fatigue_stream(client_socket)
        except: pass
        finally: client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, port))
        server.listen(100)
        while True:
            try:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port)).start()
            except: pass

    def start(self):
        self.log_event(f"[✔] HELL CORE v1.6.0: Vigilando {len(PORTS)} puertos empresariales.")
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True: time.sleep(1)

if __name__ == "__main__":
    HellServer().start()
