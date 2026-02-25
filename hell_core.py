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
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, ja3_engine, icmp_tarpit, network_mangler, bgp_emulator

# CONFIGURACIÓN HELL v7.0.0: BGP DECEPTION & ROUTING INTEL
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
K8S_PORTS = [6443, 8001]
SCADA_PORTS = [502]
ROUTING_PORTS = [179] # BGP
PORTS = WEB_PORTS + LETHAL_PORTS + K8S_PORTS + SCADA_PORTS + ROUTING_PORTS
LOG_FILE = "logs/hell_activity.log"

MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v7.0.0: BGP Router Simulation (Port 179) Active.")

    def get_routing_intel(self, ip):
        """Obtiene ASN y reputación de enrutamiento"""
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=as", timeout=3).json()
            asn = r.get('as', 'Unknown').split(' ')[0]
            reputation = bgp_emulator.check_routing_reputation(asn)
            return asn, reputation
        except: return "Unknown", "Unknown"

    def log_event(self, ip, local_port, status="START", duration=0):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if status == "START":
            asn, b_rep = self.get_routing_intel(ip)
            log_entry = f"\n[+] BGP/ROUTING TARGET DETECTED: {timestamp} | IP: {ip} | Port: {local_port}\n"
            log_entry += f"    └─ Origin ASN: {asn} | Hijack Risk: {b_rep}\n"
        else:
            log_entry = f"[-] NEUTRALIZED: {timestamp} | Held for: {round(duration, 2)}s | Mode: {status}\n"
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        start_time = time.time()
        self.log_event(ip, local_port, status="START")
        final_mode = "Tarpit"

        try:
            client_socket.settimeout(5.0)
            
            # --- MODULO BGP ---
            if local_port == 179:
                final_mode = "BGP Peer Deception"
                bgp_emulator.handle_bgp_open(client_socket, ip)
                return

            # --- OTROS MÓDULOS ---
            if local_port in SCADA_PORTS:
                scada_emulator.scada_tarpit(client_socket)
            elif local_port in [22, 2222]:
                shell_emulator.handle_mainframe_shell(client_socket, ip)
            else:
                while True: client_socket.send(b"\x00"); time.sleep(30)

        except: pass
        finally:
            duration = time.time() - start_time
            self.log_event(ip, local_port, status=final_mode, duration=duration)
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
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        # PASO 12: Network Mangler
        network_mangler.apply_mss_clamping(PORTS)
        # PASO 11: ICMP Tarpit
        threading.Thread(target=icmp_tarpit.start_icmp_tarpit, args=(self.whitelist,), daemon=True).start()
        # TCP listeners
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    HellServer().start()
