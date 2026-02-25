import socket
import threading
import time
import os
import json
import random
import requests
import signal
import sys
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing

# CONFIGURACIÓN HELL v9.1.1: DEBUG MODE
HOST = '0.0.0.0'
# Reducimos puertos inicialmente para evitar conflictos con el SSH real
PORTS = [80, 443, 445, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200]
LOG_FILE = "logs/hell_activity.log"

class HellServer:
    def __init__(self):
        print("[*] Initializing HELL CORE v9.1.1...")
        os.makedirs("logs/forensics", exist_ok=True)
        self.stats = {}
        self.active_threads = 0
        
        try:
            self.ai = predictive_ai.HellPredictiveAI()
            self.profiler = profiler_engine.HellProfiler()
            print("[+] Intelligence engines loaded.")
        except Exception as e:
            print(f"[-] Error loading engines: {e}")

        # Iniciar autolimpieza
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()
        print("[+] Self-healing monitor started.")

    def log_engagement(self, ip, port):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        report = f"\n[+] ATTACK DETECTED: {timestamp} | IP: {ip} | Port: {port}\n"
        with open(LOG_FILE, "a") as f: f.write(report)
        print(report.strip())

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        self.log_engagement(ip, local_port)
        try:
            # Tarpit simple para debug
            client_socket.send(b"HELL_READY\n")
            while True:
                client_socket.send(b"\x00")
                time.sleep(10)
        except: pass
        finally:
            client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(100)
            print(f"[✅] LISTENING ON PORT: {port}")
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except Exception as e:
            print(f"[❌] FAILED TO BIND PORT {port}: {e}")

    def start(self):
        print(f"[*] Starting listeners on {len(PORTS)} ports...")
        for port in PORTS:
            t = threading.Thread(target=self.start_listener, args=(port,), daemon=True)
            t.start()
        
        print("[🔥] HELL CORE IS FULLY OPERATIONAL.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    # Forzar salida sin buffer
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
