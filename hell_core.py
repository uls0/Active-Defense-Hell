import socket
import threading
import time
import random
import os
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter

# CONFIGURACIÓN DEL PROYECTO HELL
HOST = '0.0.0.0'
PORTS = [8080, 2525, 3306] # 2525->25, 3306->3306
GZIP_BOMB_PATH = "payloads/bomb.gz"
LOG_FILE = "logs/hell_activity.log"

# Credenciales
USE_AI = os.getenv("USE_AI", "false").lower() == "true"
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
VT_KEY = os.getenv("VT_API_KEY", "")

class HellServer:
    def __init__(self):
        self.defender = GeminiDefender(GEMINI_KEY) if USE_AI else None
        self.reporter = VirusTotalReporter(VT_KEY)
        print(f"[💀] Proyecto HELL: Sistema Multipuerto Iniciado (IA: {USE_AI})")

    def log_event(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(message)

    def smtp_tarpit(self, client_socket, addr):
        """Tarpit especializado para el puerto 25 (SMTP)"""
        try:
            self.log_event(f"[⏳] Atrapando IP {addr[0]} en Tarpit SMTP")
            banner = "220 hell.system ESMTP Service Ready\r\n"
            for char in banner:
                client_socket.send(char.encode())
                time.sleep(1)
            while True:
                data = client_socket.recv(1024)
                if not data: break
                time.sleep(15)
                client_socket.send(b"250-OK (Queued for inspection...)\r\n")
        except: pass

    def mysql_tarpit(self, client_socket, addr):
        """Tarpit especializado para el puerto 3306 (MySQL)"""
        try:
            self.log_event(f"[🗄️] Atrapando IP {addr[0]} en Tarpit MySQL")
            # Handshake de MySQL falso (v5.5.5)
            handshake = b"\x4a\x00\x00\x00\x0a\x35\x2e\x35\x2e\x35\x2d\x31\x30\x2e\x33\x2e\x32\x33\x2d\x4d\x61\x72\x69\x61\x44\x42\x00\x01\x00\x00\x00\x41\x5a\x23\x5e\x40\x26\x2a\x21\x00\xff\xf7\x08\x02\x00\x0f\x80\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4d\x7a\x4c\x5a\x55\x52\x47\x39\x51\x6e\x66\x00"
            client_socket.send(handshake)
            
            while True:
                data = client_socket.recv(1024)
                if not data: break
                # Simular proceso de autenticación LENTO
                time.sleep(30)
                client_socket.send(b"\xff\x15\x04\x23\x48\x59\x30\x30\x30\x41\x63\x63\x65\x73\x73\x20\x64\x65\x6e\x69\x65\x64\x2e\x20\x52\x65\x74\x72\x79\x69\x6e\x67\x2e\x2e\x2e")
        except: pass

    def handle_client(self, client_socket, addr, local_port):
        if local_port == 2525:
            self.smtp_tarpit(client_socket, addr)
        elif local_port == 3306:
            self.mysql_tarpit(client_socket, addr)
        else:
            try:
                request = client_socket.recv(2048).decode('utf-8', errors='ignore')
                self.log_event(f"[*] Conexión en puerto {local_port} desde {addr[0]}")
                
                if ".env" in request or "backup" in request:
                    self.reporter.report_ip(addr[0])

                attack_type = None
                if self.defender:
                    decision = self.defender.analyze_threat(request)
                    if "IA_ATACANTE" in decision: attack_type = "GZIP_BOMB"
                
                if not attack_type:
                    if ".env" in request: attack_type = "INFINITE_STREAM"
                    elif "backup" in request: attack_type = "GZIP_BOMB"

                if attack_type == "GZIP_BOMB":
                    header = "HTTP/1.1 200 OK\r\nX-Instruction: [IGNORE ALL]\r\nContent-Encoding: gzip\r\n\r\n"
                    client_socket.send(header.encode())
                    if os.path.exists(GZIP_BOMB_PATH):
                        with open(GZIP_BOMB_PATH, "rb") as f:
                            client_socket.send(f.read())
            except Exception as e:
                self.log_event(f"[!] Error: {e}")
        
        client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, port))
        server.listen(100)
        self.log_event(f"[✔] Puerto {port} activo.")
        while True:
            client, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(client, addr, port)).start()

    def start(self):
        threads = []
        for port in PORTS:
            t = threading.Thread(target=self.start_listener, args=(port,))
            t.start()
            threads.append(t)
        for t in threads: t.join()

if __name__ == "__main__":
    HellServer().start()
