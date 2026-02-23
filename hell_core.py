import socket
import threading
import time
import random
import os
import gzip
import io
import urllib.parse
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter

# CONFIGURACIÓN HELL v1.6.1: CERBERUS ACTIVE RECEIVER
HOST = '0.0.0.0'
LETHAL_PORTS = [2222, 3389, 4455]
PORTS = [8080, 2525, 3306, 6379, 1337, 8081, 8082, 2375, 8090, 8125, 8443]
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
        print(f"[💀] HELL CORE v1.6.1: RECEPTOR CERBERUS ACTIVADO")

    def log_event(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(message)

    def handle_telemetry(self, client_socket, addr, request):
        """Procesa los datos enviados por los Honey-files (Cerberus)"""
        try:
            # Extraer datos de la URL o el cuerpo POST
            self.log_event(f"[🕵️] CERBERUS BEACON: ¡Señal recibida desde el interior del atacante! ({addr[0]})")
            
            if "os=" in request or "user=" in request:
                # Intentar decodificar la información del sistema atacante
                params = urllib.parse.parse_qs(request.split("\r\n\r\n")[-1])
                user = params.get("user", ["unknown"])[0]
                os_info = params.get("os", ["unknown"])[0]
                self.log_event(f"[🕵️] INFO ATACANTE: Usuario: {user} | Sistema: {os_info}")
            
            self.reporter.report_ip(addr[0])
            client_socket.send(b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")
        except: pass

    def handle_client(self, client_socket, addr, local_port):
        if addr[0] in self.whitelist:
            client_socket.close(); return

        try:
            # Buffer de lectura más grande para capturar telemetría
            request = client_socket.recv(4096).decode('utf-8', errors='ignore')
            
            # DETECTOR GLOBAL DE TELEMETRÍA CERBERUS
            if "/api/v1/telemetry/" in request:
                self.handle_telemetry(client_socket, addr, request)
                return

            # Lógica de puertos específicos (Jenkins, Docker, Jira, etc.)
            if local_port == 8081: # Jenkins
                if "GET /credentials" in request:
                    self.log_event(f"[🕵️] Entregando Honey-tokens a {addr[0]}")
                    keys = '{"access_key": "AKIAUI7EXAMPLE", "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLE"}'
                    client_socket.send(f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{keys}".encode())
                else:
                    client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n<h1>Jenkins Dashboard</h1>")
            
            elif local_port == 1337: # Switch UI
                with open("assets/trap_1337.html", "r") as f:
                    client_socket.send(f"HTTP/1.1 200 OK\r\n\r\n{f.read()}".encode())
            
            elif local_port in LETHAL_PORTS:
                # Iniciar ataques de fatiga...
                while True: client_socket.send(os.urandom(1)); time.sleep(0.001)
            
            else:
                # Respuesta por defecto: Inundación
                while True: client_socket.send(os.urandom(4096)); time.sleep(0.1)

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
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True: time.sleep(1)

if __name__ == "__main__":
    HellServer().start()
