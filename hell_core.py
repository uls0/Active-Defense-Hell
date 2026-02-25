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
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine

# CONFIGURACIÓN HELL v8.2.3: ULTIMATE INTEL RESTORATION
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
SCADA_PORTS = [502]
PORTS = WEB_PORTS + LETHAL_PORTS + SCADA_PORTS
LOG_FILE = "logs/hell_activity.log"

MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs/malware", exist_ok=True)
        os.makedirs("logs/abuse_reports", exist_ok=True)
        self.whitelist = {MY_IP, "127.0.0.1"}
        # Diccionario para trackear daño acumulado por IP en esta sesión
        self.stats = {} 
        print(f"HELL CORE v8.2.3: Ultimate Intel Restoration complete.")

    def get_full_intel(self, ip):
        """Obtiene información forense profunda de la IP"""
        try:
            # Intentamos obtener reversa de DNS
            try: rdns = socket.gethostbyaddr(ip)[0]
            except: rdns = ip
            
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp,proxy", timeout=3).json()
            loc = f"{r.get('city', 'Unknown')}, {r.get('country', 'Unknown')}"
            asn = r.get('as', 'Unknown ASN')
            isp = r.get('isp', 'Unknown ISP')
            profile = "PROXY/VPN" if r.get('proxy') else "DATACENTER/BOT"
            return rdns, loc, asn, isp, profile
        except:
            return ip, "Unknown", "Unknown", "Unknown", "Unknown"

    def log_engagement(self, ip, port, ja3=None):
        """Log de inicio con formato ULTIMATE"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        rdns, loc, asn, isp, profile = self.get_full_intel(ip)
        
        # Actualizar contador de hits
        if ip not in self.stats:
            self.stats[ip] = {'hits': 1, 'total_time': 0, 'total_data': 0}
        else:
            self.stats[ip]['hits'] += 1

        report = (
            f"\n[+] ULTIMATE DECEPTION TRIGGERED: {timestamp}\n"
            f"----------------------------------------\n"
            f"IP: {ip} ({rdns})\n"
            f"Origin: {loc} | Profile: {profile}\n"
            f"Network: {isp} ({asn})\n"
            f"Target Port: {port} | Hit Count: {self.stats[ip]['hits']}\n"
            f"Classification: Generic Infrastructure Bot | Score: {random.randint(0,10)}\n"
            f"----------------------------------------\n"
        )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)

    def log_neutralization(self, ip, duration, bytes_sent, mode):
        """Log de cierre con formato ULTIMATE y Daño Total"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        mb_sent = round(bytes_sent / (1024 * 1024), 4)
        
        # Actualizar acumulados
        if ip in self.stats:
            self.stats[ip]['total_time'] += duration
            self.stats[ip]['total_data'] += mb_sent
        
        report = (
            f"[-] THREAT NEUTRALIZED: {timestamp}\n"
            f"    └─ Current Retention: {round(duration, 2)}s | Current Data: {mb_sent}MB\n"
            f"    └─ TOTAL DAMAGE: Time Lost: {round(self.stats[ip]['total_time'], 2)}s | Data Injected: {round(self.stats[ip]['total_data'], 2)}MB\n"
            f"    └─ Final Mitigation: {mode}\n"
            f"----------------------------------------\n"
        )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        start_time = time.time()
        final_mode = "Mitigation"
        total_bytes = 0

        # Log de inicio inmediato
        threading.Thread(target=self.log_engagement, args=(ip, local_port)).start()

        try:
            client_socket.settimeout(10.0)
            try:
                data = client_socket.recv(4096)
                req_str = data.decode('utf-8', errors='ignore')
            except: req_str = ""

            # --- LÓGICA DE CONTRA-ATAQUE ---
            if "/owa" in req_str or ".zip" in req_str or "GET / " in req_str:
                final_mode = "Fifield Ultra-Dense Attack"
                zip_generator.serve_zip_trap(client_socket)
                return
            
            if local_port in [22, 2222]:
                final_mode = "Terminal Crusher (ANSI)"
                shell_emulator.handle_mainframe_shell(client_socket, ip)
                return

            if local_port in SCADA_PORTS:
                final_mode = "SCADA Deception"
                scada_emulator.scada_tarpit(client_socket)
                return

            # Tarpit Infinito por defecto
            while True:
                client_socket.send(b"\x00")
                total_bytes += 1
                time.sleep(30)

        except: pass
        finally:
            duration = time.time() - start_time
            self.log_neutralization(ip, duration, total_bytes, final_mode)
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
        try: network_mangler.apply_mss_clamping(PORTS)
        except: pass
        
        threading.Thread(target=icmp_tarpit.start_icmp_tarpit, args=(self.whitelist,), daemon=True).start()
        
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        
        print(f"[✅] HELL CORE v8.2.3 (ULTO-INTEL) desplegado en {len(PORTS)} puertos.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    HellServer().start()
