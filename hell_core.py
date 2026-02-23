import socket
import threading
import time
import random
import os
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter

# CONFIGURACIÓN DEL PROYECTO HELL
HOST = '0.0.0.0'
PORTS = [8080, 2525] # 2525 se mapeará al 25 en Docker
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
            self.log_event(f"[⏳] Atrapando IP {addr[0]} en Tarpit SMTP (Puerto 25)")
            
            # Enviar banner LENTO (220)
            banner = "220 hell.system ESMTP Service Ready\r\n"
            for char in banner:
                client_socket.send(char.encode())
                time.sleep(1) # Un segundo por caracter para desesperar al bot
            
            while True:
                data = client_socket.recv(1024)
                if not data: break
                
                # Cualquier comando recibe una respuesta lenta y basura
                time.sleep(15) # Esperar 15 segundos antes de responder
                client_socket.send(b"250-OK (Processing heavy payload...)\r\n250-PIPELINING\r\n250 SIZE 50000000\r\n")
                
        except:
            self.log_event(f"[✔] Atacante SMTP {addr[0]} se ha rendido.")

    def handle_client(self, client_socket, addr, local_port):
        if local_port == 2525:
            self.smtp_tarpit(client_socket, addr)
            client_socket.close()
            return

        try:
            request = client_socket.recv(2048).decode('utf-8', errors='ignore')
            self.log_event(f"[*] Conexión en puerto {local_port} desde {addr[0]}")
            
            # Reportar a VirusTotal si hay actividad sospechosa
            if ".env" in request or "backup" in request:
                self.reporter.report_ip(addr[0])

            # Lógica de defensa (IA / Clásica)
            attack_type = None
            if self.defender:
                decision = self.defender.analyze_threat(request)
                if "IA_ATACANTE" in decision: attack_type = "GZIP_BOMB"
            
            if not attack_type:
                if ".env" in request: attack_type = "INFINITE_STREAM"
                elif "backup" in request: attack_type = "GZIP_BOMB"

            if attack_type == "GZIP_BOMB":
                header = "HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\n\r\n"
                client_socket.send(header.encode())
                if os.path.exists(GZIP_BOMB_PATH):
                    with open(GZIP_BOMB_PATH, "rb") as f:
                        client_socket.send(f.read())
        except Exception as e:
            self.log_event(f"[!] Error: {e}")
        finally:
            client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, port))
        server.listen(100)
        self.log_event(f"[✔] Escuchando en puerto {port}")
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
