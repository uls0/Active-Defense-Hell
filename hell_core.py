import socket
import threading
import time
import random
import os
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter

# CONFIGURACIÓN EXPANDIDA DEL PROYECTO HELL
HOST = '0.0.0.0'
# Mapeo: 8080(Web), 2525(SMTP), 3306(MySQL), 2222(SSH), 3389(RDP), 6379(Redis), 4455(SMB)
PORTS = [8080, 2525, 3306, 2222, 3389, 6379, 4455]
GZIP_BOMB_PATH = "payloads/bomb.gz"
LOG_FILE = "logs/hell_activity.log"

USE_AI = os.getenv("USE_AI", "false").lower() == "true"
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
VT_KEY = os.getenv("VT_API_KEY", "")

class HellServer:
    def __init__(self):
        self.defender = GeminiDefender(GEMINI_KEY) if USE_AI else None
        self.reporter = VirusTotalReporter(VT_KEY)
        print(f"[💀] PROYECTO HELL: MODO ENTROPÍA TOTAL ACTIVADO")

    def log_event(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(message)

    def generate_garbage(self, size=1024):
        """Genera basura binaria aleatoria"""
        return os.urandom(size)

    def universal_garbage_stream(self, client_socket, addr):
        """Bucle infinito de basura para cualquier conexión no identificada"""
        self.log_event(f"[🌊] INUNDANDO IP {addr[0]} con datos basura...")
        try:
            while True:
                junk = self.generate_garbage(4096)
                client_socket.send(junk)
                time.sleep(0.1) # 40KB/s de pura entropía
        except: pass

    def handle_client(self, client_socket, addr, local_port):
        self.log_event(f"[*] Atrapado: {addr[0]} en puerto {local_port}")
        
        try:
            # Reportar a VirusTotal preventivamente
            self.reporter.report_ip(addr[0])

            if local_port == 2222: # SSH Tarpit
                client_socket.send(b"SSH-2.0-OpenSSH_8.2p1\r\n")
                time.sleep(5)
                self.universal_garbage_stream(client_socket, addr)
            
            elif local_port == 2525: # SMTP Tarpit
                client_socket.send(b"220 hell.smtp ESMTP\r\n")
                time.sleep(10)
                self.universal_garbage_stream(client_socket, addr)

            elif local_port == 3306 or local_port == 6379: # DB Tarpit
                self.universal_garbage_stream(client_socket, addr)

            else:
                # Lógica Web / Genérica
                request = client_socket.recv(2048).decode('utf-8', errors='ignore')
                
                # Contraataque de IA o Bombas
                if "backup" in request or "admin" in request:
                    self.log_event(f"[🔥] LANZANDO GZIP BOMB contra {addr[0]}")
                    header = "HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\n\r\n"
                    client_socket.send(header.encode())
                    if os.path.exists(GZIP_BOMB_PATH):
                        with open(GZIP_BOMB_PATH, "rb") as f: client_socket.send(f.read())
                
                # Por defecto: Basura infinita
                self.universal_garbage_stream(client_socket, addr)

        except Exception as e:
            self.log_event(f"[!] Conexión cerrada con {addr[0]}: {e}")
        finally:
            client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, port))
        server.listen(100)
        while True:
            client, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(client, addr, port)).start()

    def start(self):
        self.log_event(f"[✔] HELL Core a la escucha en {len(PORTS)} puertos.")
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,)).start()

if __name__ == "__main__":
    HellServer().start()
