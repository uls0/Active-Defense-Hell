import socket
import threading
import time
import os
import sys
import json
import random
import requests
import signal
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing, canary_generator, malware_triage, network_simulator

VERSION = "v10.2.1-SINGULARITY"
LOG_FILE = "logs/hell_activity.log"
INTEL_FILE = "logs/mesh_intel.json"
HOST = '0.0.0.0'
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200, 4455]

class HellServer:
    def __init__(self):
        print(f"[*] DEPLOYING {VERSION} | FINAL MASTER CORE")
        os.makedirs("logs/forensics", exist_ok=True)
        os.makedirs("logs/malware", exist_ok=True)
        self.stats = {}
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        start_time = time.time()
        ja3_hash = None
        if local_port in [443, 8443]:
            try: ja3_hash = ja3_engine.get_ja3_hash(client_socket.recv(1024, socket.MSG_PEEK))
            except: pass

        total_bytes = 0
        final_mode = "Mitigation"

        try:
            client_socket.settimeout(15.0)
            data = client_socket.recv(8192)
            req_str = data.decode('utf-8', errors='ignore')

            # Malware Triage Logic
            if "POST" in req_str or "PUT" in req_str or b"\x7fELF" in data:
                final_mode = "Malware Captured"
                sample_path = malware_triage.save_sample(data, ip)
                threading.Thread(target=malware_triage.perform_triage, args=(sample_path, os.getenv("VT_API_KEY")), daemon=True).start()
                zip_generator.serve_zip_trap(client_socket)
                return

            if local_port in [445, 4455]:
                final_mode = "AD-Labyrinth"
                total_bytes = smb_lethal.handle_smb_session(client_socket, ip)
                return

            if local_port == 22:
                final_mode = "Bait-Switch"
                shell_emulator.handle_cowrie_trap(client_socket, ip)
                return

            while True:
                client_socket.send(b"\x00")
                total_bytes += 1024; time.sleep(30)

        except: pass
        finally:
            duration = time.time() - start_time
            mb = round(total_bytes / (1024*1024), 4)
            with open(LOG_FILE, "a") as f:
                f.write(f"[-] NEUTRALIZED: {time.ctime()} | Held: {round(duration,2)}s | Data: {mb}MB | Mode: {final_mode}\n")
            client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port))
            server.listen(500)
            print(f"[✅] Port {port}: ARMED")
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except: pass

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        print(f"[🚀] {VERSION} IS ACTIVE. SOBERANÍA DIGITAL ASEGURADA.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
