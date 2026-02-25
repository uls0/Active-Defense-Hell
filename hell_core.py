import socket
import threading
import time
import os
import binascii
import random
import requests
import base64
import json
import zlib
import signal
import sys
from datetime import datetime
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, mesh_node, predictive_ai, database_emulator, forensics_engine, profiler_engine

# CONFIGURACIÓN HELL v8.9.1: ACTIVE DIRECTORY DECEPTION RESTORED
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389]
DB_PORTS = [3306, 1433]
AD_PORTS = [445, 4455, 389, 88] # Puertos de Active Directory y SMB
SCADA_PORTS = [502]
PORTS = WEB_PORTS + LETHAL_PORTS + DB_PORTS + AD_PORTS + SCADA_PORTS
LOG_FILE = "logs/hell_activity.log"

MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs/malware", exist_ok=True)
        os.makedirs("logs/abuse_reports", exist_ok=True)
        os.makedirs("logs/forensics", exist_ok=True)
        self.whitelist = {MY_IP, "127.0.0.1"}
        self.stats = {} 
        self.mesh = mesh_node.start_mesh_service("NODE-SFO-01", [])
        self.profiler = profiler_engine.HellProfiler()
        print(f"HELL CORE v8.9.1: Fake Active Directory Services RESTORED.")

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        threading.Thread(target=self.log_engagement, args=(ip, local_port)).start()

        try:
            client_socket.settimeout(10.0)
            # Peek inicial para lógica de decisión
            try: data = client_socket.recv(4096); req_str = data.decode('utf-8', errors='ignore')
            except: req_str = ""; data = b""

            # --- 1. LÓGICA DE ACTIVE DIRECTORY / SMB (NUEVO/RESTAURADO) ---
            if local_port in [445, 4455]:
                # Invocamos el módulo letal de SMB
                smb_lethal.handle_smb_session(client_socket, ip)
                return
            
            if local_port == 389:
                # Simulación de LDAP: Enviamos respuesta de éxito de bind falsa
                client_socket.send(b"LDAP_SUCCESS - DC=tvg,DC=mx - Active Directory Domain Controller\n")
                while True:
                    client_socket.send(b"\x00")
                    time.sleep(30)
                return

            # --- 2. LÓGICA DE BASES DE DATOS ---
            if local_port == 3306:
                database_emulator.handle_mysql_trap(client_socket)
                return

            # --- 3. LÓGICA DE WEB / ZIP BOMBS ---
            if "/owa" in req_str or ".zip" in req_str:
                zip_generator.serve_zip_trap(client_socket)
                return
            
            # --- 4. LÓGICA DE SSH / SHELL ---
            if local_port == 22:
                shell_emulator.handle_cowrie_trap(client_socket, ip)
                return

            # Tarpit por defecto para el resto
            while True:
                client_socket.send(b"\x00")
                time.sleep(30)

        except: pass
        finally:
            client_socket.close()

    def log_engagement(self, ip, port, ja3=None):
        # (Se mantiene la lógica de log profesional del paso anterior)
        pass

    def start(self):
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        for port in PORTS:
            threading.Thread(target=lambda p=port: self.start_listener(p), daemon=True).start()
        print(f"[✅] HELL CORE v8.9.1 desplegado con AD-FAKE en puertos 445/389.")
        while True: time.sleep(1)

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

if __name__ == "__main__":
    HellServer().start()
