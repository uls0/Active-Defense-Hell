import socket
import threading
import time
import os
import sys
import json
import random
import requests
import signal

print("[*] BOOT: Starting HELL CORE v9.1.3 - Tactical Edition")

# --- BLOQUE DE IMPORTACIÓN PROTEGIDA ---
try:
    from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing
    print("[+] BOOT: All tactical modules loaded successfully.")
except Exception as e:
    print(f"[❌] BOOT FATAL ERROR: Could not load modules: {e}")
    sys.exit(1)

# CONFIGURACIÓN
HOST = '0.0.0.0'
# Puertos de alta prioridad (Excluimos el 22 si hay conflicto)
PORTS = [80, 443, 445, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200]
LOG_FILE = "logs/hell_activity.log"

class HellServer:
    def __init__(self):
        os.makedirs("logs/forensics", exist_ok=True)
        self.stats = {}
        self.active_threads = 0
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        
        # Iniciar mantenimiento en segundo plano
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()
        print("[+] BOOT: Self-healing and AI engines online.")

    def log_engagement(self, ip, port):
        """Formato Forense Legacy Restaurado"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if ip not in self.stats: self.stats[ip] = {'hits': 1}
        else: self.stats[ip]['hits'] += 1

        report = (
            f"\n[+] ULTIMATE DECEPTION TRIGGERED: {timestamp}\n"
            f"----------------------------------------\n"
            f"IP: {ip} | Target Port: {port}\n"
            f"Session Hits: {self.stats[ip]['hits']}\n"
            f"Status: ACTIVE ENGAGEMENT\n"
            f"----------------------------------------\n"
        )
        print(f"[🔥] Target Engaged: {ip}:{port}")
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        self.active_threads += 1
        self.log_engagement(ip, local_port)

        try:
            client_socket.settimeout(10.0)
            
            # Lógica de respuesta por puerto
            if local_port in [445, 4455]:
                smb_lethal.handle_smb_session(client_socket, ip)
            elif local_port in [22, 2222]:
                shell_emulator.handle_cowrie_trap(client_socket, ip)
            elif local_port == 3306:
                database_emulator.handle_mysql_trap(client_socket)
            else:
                # Tarpit genérico
                while True:
                    client_socket.send(b"\x00")
                    time.sleep(30)
        except: pass
        finally:
            self.active_threads -= 1
            try: client_socket.close()
            except: pass

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(150)
            print(f"[✅] SERVICE READY ON PORT: {port}")
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except Exception as e:
            print(f"[⚠️] PORT {port} UNAVAILABLE: {e}")

    def start(self):
        print(f"[*] Deploying listeners on {len(PORTS)} targets...")
        for port in PORTS:
            t = threading.Thread(target=self.start_listener, args=(port,), daemon=True)
            t.start()
        
        print("[🚀] HELL CORE v9.1.3 IS LIVE AND HUNGRY.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    # Forzar salida inmediata a Docker
    sys.stdout.reconfigure(line_buffering=True)
    server = HellServer()
    server.start()
