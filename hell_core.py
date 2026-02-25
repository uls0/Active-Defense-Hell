import socket
import threading
import time
import os
import binascii
import random
import requests
import base64
import hashlib
import json
import zlib
import signal
import sys
from datetime import datetime
from threat_intel import VirusTotalReporter, IsMaliciousReporter
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, ja3_engine, icmp_tarpit, network_mangler

# CONFIGURACIÓN HELL v6.9.0: MTU MISMATCHING & NETWORK CRUSHER
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
K8S_PORTS = [6443, 8001]
SCADA_PORTS = [502]
PORTS = WEB_PORTS + LETHAL_PORTS + K8S_PORTS + SCADA_PORTS
LOG_FILE = "logs/hell_activity.log"

MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v6.9.0: Network Evasion Layer fully operational.")

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        try:
            client_socket.settimeout(5.0)
            # --- MODULOS DE DECEPCIÓN ---
            if local_port in SCADA_PORTS:
                scada_emulator.scada_tarpit(client_socket)
            elif local_port in [22, 2222]:
                shell_emulator.handle_mainframe_shell(client_socket, ip)
            else:
                while True: client_socket.send(b"\x00"); time.sleep(30)
        except: pass
        finally: client_socket.close()

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

    def signal_handler(self, sig, frame):
        print("\n[!] Apagando HELL...")
        network_mangler.cleanup_mss_rules(PORTS)
        sys.exit(0)

    def start(self):
        # Manejador para limpieza de reglas al salir
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # PASO 12: Aplicar MSS Clamping
        network_mangler.apply_mss_clamping(PORTS)
        
        # PASO 11: Iniciar ICMP Tarpit
        threading.Thread(target=icmp_tarpit.start_icmp_tarpit, args=(self.whitelist,), daemon=True).start()
        
        # Iniciar TCP listeners
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        
        print("[🔥] HELL v6.9.0 está listo para devorar bots.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    HellServer().start()
