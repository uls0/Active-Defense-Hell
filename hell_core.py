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

# CONFIGURACIÓN HELL v2.1.0: INTELLIGENCE & PORT SYNC
HOST = '0.0.0.0'
LETHAL_PORTS = [2222, 3389, 4455]
# Ahora sumamos todos los puertos para el listener
PORTS = [8080, 2525, 3306, 6379, 1337, 8081, 8082, 2375, 8090, 8125, 8443] + LETHAL_PORTS
GZIP_BOMB_PATH = "payloads/bomb.gz"
LOG_FILE = "logs/hell_activity.log"

USE_AI = os.getenv("USE_AI", "false").lower() == "true"
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
VT_KEY = os.getenv("VT_API_KEY", "")
MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.defender = GeminiDefender(GEMINI_KEY) if USE_AI else None
        self.reporter = VirusTotalReporter(VT_KEY)
        self.whitelist = {MY_IP, "127.0.0.1"}
        # Verificar API de VirusTotal al iniciar
        if VT_KEY: print("[📡] Módulo VirusTotal: Activo y listo para reportar.")
        print(f"[💀] HELL CORE v2.1.0: Vigilando {len(PORTS)} puertos en total.")

    def log_event(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        try:
            with open(LOG_FILE, "a", encoding='utf-8') as f:
                f.write(log_entry)
                f.flush()
            print(log_entry.strip())
        except: pass

    def handle_client(self, client_socket, addr, local_port):
        if addr[0] in self.whitelist:
            client_socket.close(); return

        try:
            # Reportar preventivamente
            self.log_event(f"[*] Hit detectado: {addr[0]} en puerto {local_port}")
            self.reporter.report_ip(addr[0])

            # Lógica de respuesta (Resumen para brevedad)
            if local_port in [2222, 3389, 4455]: # Lethal fatigue
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
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True: time.sleep(1)

if __name__ == "__main__":
    HellServer().start()
