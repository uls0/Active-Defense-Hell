import socket
import threading
import time
import os
import binascii
import random
import requests
import zlib
from datetime import datetime
from threat_intel import VirusTotalReporter, IsMaliciousReporter
from scripts import smb_lethal

# CONFIGURACIÓN HELL v4.9.0: BOT ANCHORING & DRIP-FEED
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
RAW_PORTS = [21, 23, 25, 1433, 2323, 2525, 3306, 6379, 1337, 2375, 8125, 5060, 5900, 110, 5555]
AD_PORTS = [53, 88, 135, 389, 636, 3268, 5985]
AI_PORTS = [11434, 8188, 1234, 3000]
VULN_PORTS = [10443]

PORTS = WEB_PORTS + LETHAL_PORTS + RAW_PORTS + AD_PORTS + AI_PORTS + VULN_PORTS
LOG_FILE = "logs/hell_activity.log"

VT_KEY = os.getenv("VT_API_KEY", "")
ISM_KEY = "b0959d3e-97c6-451f-9f95-5148c2da7ddd"
ISM_SECRET = "643a5731-1af4-4632-b75c-65955138288a"
MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v4.9.0: Bot Anchoring & Drip-Feed Enabled. Sockets are now sticky.")

    def log_event(self, ip, local_port, scanner, status="START", duration=0, bytes_sent=0):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if status == "START":
            log_entry = f"\n[+] STICKY TARGET DETECTED: {timestamp} | IP: {ip} | Port: {local_port}\n"
        else:
            mb_sent = round(bytes_sent / (1024 * 1024), 4)
            log_entry = f"[-] TARGET RELEASED: {timestamp} | Held for: {round(duration, 2)}s | Data: {mb_sent}MB | Strategy: {status}\n"
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def anchored_send(self, client_socket, data, interval=5):
        """Envía datos goteando byte a byte para evitar desconexiones por timeout"""
        total = 0
        try:
            for byte in data:
                # Si el dato es int (de un bytearray), lo convertimos a bytes
                b = bytes([byte]) if isinstance(byte, int) else byte.encode()
                client_socket.send(b)
                total += 1
                # Goteo: Retraso sutil pero efectivo
                time.sleep(random.uniform(0.1, 0.5))
        except: pass
        return total

    def keep_alive_heartbeat(self, client_socket):
        """Mantiene la conexión enviando un 'latido' de bytes nulos periódicamente"""
        total = 0
        while True:
            try:
                # Enviamos un espacio en blanco o un byte nulo cada 15-20 segundos
                heartbeat = random.choice([b"\x20", b"\x00", b"\r\n"])
                client_socket.send(heartbeat)
                total += len(heartbeat)
                time.sleep(random.randint(15, 25))
            except:
                break
        return total

    def serve_zlib_bomb(self, client_socket):
        """Bomba Zlib con Drip-Feed para máximo anclaje"""
        payload = b"\x00" * (1024 * 1024 * 50) # 50MB que se expanden
        compressed = zlib.compress(payload)
        header = (
            "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
            "Content-Encoding: deflate\r\nConnection: keep-alive\r\n\r\n"
        )
        client_socket.send(header.encode())
        # Enviamos la bomba goteando para que el bot no pueda dejar de leer
        return len(header) + self.anchored_send(client_socket, compressed)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        start_time = time.time()
        total_bytes_sent = 0
        strategy = "Anchored Retention"

        try:
            client_socket.settimeout(30.0) # Aumentamos el timeout interno para el anclaje
            self.log_event(ip, local_port, "Sticky Bot", status="START")

            # --- ESTRATEGIA DE ANCLAJE ---
            
            if local_port in AI_PORTS:
                strategy = "Anchored AI Zlib Bomb"
                total_bytes_sent += self.serve_zlib_bomb(client_socket)
            
            elif local_port in WEB_PORTS:
                strategy = "HTTP Heartbeat Tarpit"
                header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nTransfer-Encoding: chunked\r\n\r\n"
                client_socket.send(header.encode())
                total_bytes_sent += len(header)
                # Inyectar el corazón de la trampa
                total_bytes_sent += self.keep_alive_heartbeat(client_socket)

            elif local_port in LETHAL_PORTS:
                strategy = "L4 Drip-Feed Tarpit"
                # Enviamos basura pero byte a byte muy lentamente
                while True:
                    client_socket.send(os.urandom(1))
                    total_bytes_sent += 1
                    time.sleep(random.randint(10, 20))
            
            elif local_port == 445:
                strategy = "SMB Lethal Maze"
                total_bytes_sent = smb_lethal.handle_smb_attack(client_socket, ip, (lambda *args, **kwargs: None), local_port)
            
            else:
                strategy = "Infinite Heartbeat Stream"
                total_bytes_sent += self.keep_alive_heartbeat(client_socket)

        except: pass
        finally:
            duration = time.time() - start_time
            self.log_event(ip, local_port, None, status=strategy, duration=duration, bytes_sent=total_bytes_sent)
            try: client_socket.close()
            except: pass

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(100)
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except: pass

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    HellServer().start()
