import socket
import threading
import time
import os
import binascii
import random
import requests
from datetime import datetime
from threat_intel import VirusTotalReporter, IsMaliciousReporter

# CONFIGURACIÓN HELL v3.0.0: SATURATION & MEXICAN DECEPTION
HOST = '0.0.0.0'

# Puertos Especializados
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455] # Incluimos Puerto 22
RAW_PORTS = [21, 23, 25, 445, 1433, 2323, 2525, 3306, 6379, 1337, 2375, 8125, 5060, 5900, 110, 5555]

# Generar lista de saturación (Top 100 Nmap saltando los ya usados)
TOP_100_NMAP = [1, 3, 7, 9, 13, 17, 19, 21, 22, 23, 25, 26, 37, 53, 79, 80, 81, 88, 106, 110, 111, 113, 119, 135, 139, 143, 144, 179, 199, 389, 427, 443, 444, 445, 465, 513, 514, 515, 543, 544, 548, 554, 587, 631, 646, 873, 990, 993, 995, 1025, 1026, 1027, 1028, 1029, 1110, 1433, 1720, 1723, 1755, 1900, 2000, 2049, 2121, 2717, 3000, 3128, 3306, 3389, 3986, 4899, 5000, 5009, 5051, 5060, 5101, 5190, 5357, 5432, 5631, 5666, 5800, 5900, 6000, 6001, 6646, 7070, 8000, 8008, 8009, 8080, 8081, 8443, 8888, 9100, 9999, 10000, 32768, 49152, 49153, 49154, 49155, 49156, 49157]
SATURATION_PORTS = list(set(TOP_100_NMAP) - set(WEB_PORTS) - set(LETHAL_PORTS) - set(RAW_PORTS))

PORTS = WEB_PORTS + LETHAL_PORTS + RAW_PORTS + SATURATION_PORTS
LOG_FILE = "logs/hell_activity.log"

VT_KEY = os.getenv("VT_API_KEY", "")
ISM_KEY = "b0959d3e-97c6-451f-9f95-5148c2da7ddd"
ISM_SECRET = "643a5731-1af4-4632-b75c-65955138288a"

# Tracker de Port-Hopping {ip: [puertos_visitados]}
scan_sequences = {}
persistent_offenders = {}

# Banners Mexicanos Dinámicos
MEXICAN_BANNERS = {
    21: "220 (vsFTPd 3.0.5) - Nodo-Transferencia-Pemex-Logistica\r\n",
    22: "SSH-2.0-OpenSSH_8.9p1 (SISTEMAS-BANXICO-NODE-04)\r\n",
    23: "\r\nAcceso Restringido - Red Interna Telmex-Infinitum\r\nlogin: ",
    25: "220 mail.gob.mx ESMTP Postfix - Secretaria de Hacienda\r\n",
    110: "+OK POP3 Ready (Servidor de Correo Corporativo Soriana)\r\n",
    1433: "MSSQL Server 2019 - Node: MX-CORP-DATA-01\r\n",
    3306: "5.7.33-0ubuntu0.18.04.1 (MySQL-Server-Bimbo-Produccion)\r\n"
}

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        print(f"HELL CORE v3.0.0: MODO SATURACION ACTIVADO. {len(PORTS)} puertos abiertos.")

    def track_scan(self, ip, port):
        """Detecta patrones de escaneo secuencial"""
        if ip not in scan_sequences: scan_sequences[ip] = []
        scan_sequences[ip].append(port)
        if len(scan_sequences[ip]) > 3:
            seq = scan_sequences[ip][-3:]
            # Si los últimos 3 puertos son seguidos (ej 21, 22, 23)
            if abs(seq[0] - seq[1]) <= 2 and abs(seq[1] - seq[2]) <= 2:
                return True
        return False

    def log_event(self, ip, local_port, scanner, status="START", intel=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{status}] IP: {ip} | Port: {local_port} | Signature: {scanner} | Hits: {persistent_offenders.get(ip, 1)}\n"
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        persistent_offenders[ip] = persistent_offenders.get(ip, 0) + 1
        is_hopping = self.track_scan(ip, local_port)
        
        try:
            client_socket.settimeout(10.0)
            scanner_type = "Unknown"
            
            # --- FASE 1: BANNER DECEPCION ---
            if local_port in MEXICAN_BANNERS:
                client_socket.send(MEXICAN_BANNERS[local_port].encode())
            
            # Recibir datos para identificar escaner
            try: data = client_socket.recv(1024)
            except: data = b""
            
            self.log_event(ip, local_port, "Active Bot", status="HIT")

            # --- FASE 2: CONTRAMEDIDAS ---

            # A. KILLSWITCH PARA PORT-HOPPING
            if is_hopping:
                print(f"Port-Hopping detectado desde {ip}. Enviando Garbage Killswitch.")
                # Enviar basura de alta entropía que rompe parsers de Nmap
                client_socket.send(os.urandom(1024) + b"\x00\xff\x00\xff")
                time.sleep(1)
                return

            # B. SMB TRAP AVANZADO (Pending Status)
            if local_port == 445 or b"SMB" in data:
                # Responder con un paquete SMB2 "STATUS_PENDING"
                pending_pkt = binascii.unhexlify("fe534d4240000000050000000000000000000000000000000000000000000000")
                client_socket.send(pending_pkt)
                while True:
                    time.sleep(30)
                    client_socket.send(b"\x00")

            # C. LETHAL TARPIT (Port 22, 3389, etc)
            elif local_port in LETHAL_PORTS:
                while True:
                    client_socket.send(os.urandom(1))
                    time.sleep(random.randint(10, 20))

            # D. SATURACION GENERAL
            else:
                while True:
                    client_socket.send(os.urandom(1024))
                    time.sleep(1)

        except: pass
        finally:
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
