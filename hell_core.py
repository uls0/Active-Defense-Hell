import socket
import threading
import time
import os
import sys
import requests
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing

print("[*] BOOT: HELL CORE v9.3.0 - Bait & Switch Edition")

HOST = '0.0.0.0'
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200]
LOG_FILE = "logs/hell_activity.log"

class HellServer:
    def __init__(self):
        os.makedirs("logs/forensics", exist_ok=True)
        self.stats = {} # {ip: {'hits': X, 'ports': [], ...}}
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def log_engagement(self, ip, port):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if ip not in self.stats: self.stats[ip] = {'hits': 1}
        else: self.stats[ip]['hits'] += 1
        
        hit_count = self.stats[ip]['hits']
        report = f"\n[+] BAIT-SWITCH ENGAGED: {timestamp} | IP: {ip} | Port: {port} | Identity Cycle: {hit_count % 4}\n"
        with open(LOG_FILE, "a") as f: f.write(report)
        print(f"[🔥] Target Engaged: {ip}:{port} (Hit #{hit_count})")
        return hit_count

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        hit_count = self.log_engagement(ip, local_port)
        try:
            client_socket.settimeout(15.0)
            if local_port in [445, 4455]:
                smb_lethal.handle_smb_session(client_socket, ip)
            elif local_port == 22:
                # Pasamos hit_count para cambiar la identidad
                shell_emulator.handle_cowrie_trap(client_socket, ip, hit_count)
            elif local_port == 2222:
                shell_emulator.handle_mainframe_shell(client_socket, ip)
            elif local_port == 3306:
                database_emulator.handle_mysql_trap(client_socket)
            else:
                while True:
                    client_socket.send(b"\x00")
                    time.sleep(20)
        except: pass
        finally:
            try: client_socket.close()
            except: pass

    def start_listener(self, port):
        while True:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                server.bind((HOST, port))
                server.listen(200)
                print(f"[✅] LISTENING: Port {port}")
                while True:
                    client, addr = server.accept()
                    threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
            except: time.sleep(10)

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        print("[🚀] HELL v9.3.0: BAIT & SWITCH ACTIVE.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
