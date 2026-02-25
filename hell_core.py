import socket
import threading
import time
import os
import sys
import json
import random
import requests
import signal
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing

print("💀 HELL CORE v9.4.2-ULTIMATE: Rapid Forensics Active.")

HOST = '0.0.0.0'
# Incluimos explícitamente el 4455 que es el que están atacando más
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200, 4455]
LOG_FILE = "logs/hell_activity.log"

class HellServer:
    def __init__(self):
        os.makedirs("logs/forensics", exist_ok=True)
        os.makedirs("logs/malware", exist_ok=True)
        self.stats = {}
        self.active_threads = 0
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def log_neutralization(self, ip, duration, bytes_sent, mode):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        mb_sent = round(bytes_sent / (1024 * 1024), 4)
        if ip in self.stats:
            self.stats[ip]['total_time'] += duration
            self.stats[ip]['total_data'] += mb_sent
        
        report = (
            f"[-] THREAT NEUTRALIZED: {timestamp}\n"
            f"    └─ Current Retention: {round(duration, 2)}s | Data: {mb_sent}MB\n"
            f"    └─ TOTAL DAMAGE: Time Lost: {round(self.stats[ip]['total_time'], 2)}s | Injected: {round(self.stats[ip]['total_data'], 2)}MB\n"
            f"    └─ Final Mitigation: {mode}\n"
            f"----------------------------------------\n"
        )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)
        
        # UMBRAL RAPID FORENSICS: 60 SEGUNDOS
        if duration > 60:
            forensics_engine.create_evidence_pack(ip, timestamp)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        # (Lógica de log_engagement aquí...)
        
        start_time = time.time()
        final_mode = "Mitigation"
        total_bytes = 0

        try:
            client_socket.settimeout(15.0)
            if local_port in [445, 4455]:
                smb_lethal.handle_smb_session(client_socket, ip)
                return
            # [Resto de lógica igual...]
        except: pass
        finally:
            self.log_neutralization(ip, time.time() - start_time, total_bytes, final_mode)
            try: client_socket.close()
            except: pass

    def start_listener(self, port):
        while True:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                server.bind((HOST, port))
                server.listen(300)
                print(f"[✅] Port {port}: ACTIVE")
                while True:
                    client, addr = server.accept()
                    threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
            except: time.sleep(5)

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True: time.sleep(1)

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
