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
from threat_intel import VirusTotalReporter, IsMaliciousReporter
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine

# CONFIGURACIÓN HELL v8.2.1: STABLE BURNOUT & ABUSE REPORTING
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
        print(f"HELL CORE v8.2.1: Stable Resource Exhaustion Active.")

    def get_full_intel(self, ip):
        """Obtiene ASN y Ubicación para el reporte de abuso"""
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as", timeout=3).json()
            loc = f"{r.get('city')}, {r.get('country')}"
            asn = r.get('as', 'Unknown')
            return asn, loc
        except: return "Unknown", "Unknown"

    def log_event(self, ip, local_port, status="START", duration=0, bytes_sent=0, ja3=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        mb_sent = round(bytes_sent / (1024 * 1024), 2)
        
        if status == "START":
            log_entry = f"\n[🔥] TARGET ENGAGED: {timestamp} | IP: {ip} | Port: {local_port}\n"
        else:
            log_entry = f"[-] EXHAUSTED: {timestamp} | Held: {round(duration, 2)}s | Impact: {mb_sent}MB | Mode: {status}\n"
            # Generar reporte si el daño es significativo (>120s o >5MB)
            if duration > 120 or mb_sent > 5:
                asn, loc = self.get_full_intel(ip)
                abuse_generator.generate_formal_report(ip, asn, loc, ja3, duration, mb_sent)
        
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        start_time = time.time()
        final_mode = "Mitigation"
        ja3_hash = None
        total_bytes = 0

        try:
            client_socket.settimeout(10.0)
            
            # --- TLS Fingerprinting (JA3) ---
            if local_port in [443, 8443]:
                try:
                    peek_data = client_socket.recv(1024, socket.MSG_PEEK)
                    ja3_hash = ja3_engine.get_ja3_hash(peek_data)
                except: pass

            self.log_event(ip, local_port, status="START", ja3=ja3_hash)
            
            # Recepción inicial de datos
            try:
                data = client_socket.recv(4096)
                req_str = data.decode('utf-8', errors='ignore')
            except: req_str = ""

            # --- LÓGICA DE CONTRA-ATAQUE (FIFIELD BOMB / TERMINAL CRUSHER) ---
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

            # Tarpit Infinito para puertos genéricos
            while True:
                client_socket.send(b"\x00")
                total_bytes += 1
                time.sleep(30)

        except: pass
        finally:
            duration = time.time() - start_time
            self.log_event(ip, local_port, status=final_mode, duration=duration, bytes_sent=total_bytes, ja3=ja3_hash)
            try: client_socket.close()
            except: pass

    def start_listener(self, port):
        """Escuchador de puerto individual"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(100)
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except Exception as e:
            print(f"[!] Error en puerto {port}: {e}")

    def start(self):
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        
        # Aplicar MSS Clamping (Requiere Root en el host)
        try: network_mangler.apply_mss_clamping(PORTS)
        except: print("[!] MSS Clamping falló. Requiere privilegios root.")
        
        # Tarpit ICMP (Ping)
        threading.Thread(target=icmp_tarpit.start_icmp_tarpit, args=(self.whitelist,), daemon=True).start()
        
        # Iniciar escuchadores TCP
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        
        print(f"[✅] HELL CORE v8.2.1 desplegado en {len(PORTS)} puertos.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    HellServer().start()
