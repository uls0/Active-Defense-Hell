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

VERSION = "v10.0.0-SINGULARITY"
LOG_FILE = "logs/hell_activity.log"
HOST = '0.0.0.0'
PORTS = [80, 443, 445, 22, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200, 4455]

class HellServer:
    def __init__(self):
        print(f"[*] INITIALIZING {VERSION} | THE ULTIMATE DEFENSE")
        os.makedirs("logs/forensics", exist_ok=True)
        self.stats = {}
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def log_engagement(self, ip, port):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if ip not in self.stats: self.stats[ip] = {'hits': 1, 'ports': [port], 'commands': []}
        else: self.stats[ip]['hits'] += 1
        
        actor, conf = self.profiler.classify_attacker(self.stats[ip]['commands'], None, self.stats[ip]['ports'])
        report = (
            f"\n[+] TRIGGERED: {timestamp}\n"
            f"IP: {ip} | Actor: {actor}({conf}%)\n"
            f"Target Port: {port} | Session Hits: {self.stats[ip]['hits']}\n"
            f"----------------------------------------\n"
        )
        with open(LOG_FILE, "a") as f: f.write(report)
        print(f"[🔥] {actor} ENGAGED on {port}")

    def handle_client(self, client_socket, addr, local_port):
        self.log_engagement(addr[0], local_port)
        try:
            client_socket.settimeout(15.0)
            if local_port in [445, 4455]: smb_lethal.handle_smb_session(client_socket, addr[0])
            elif local_port == 22: shell_emulator.handle_cowrie_trap(client_socket, addr[0])
            elif local_port == 3306: database_emulator.handle_mysql_trap(client_socket)
            else:
                while True:
                    client_socket.send(b"\x00")
                    time.sleep(30)
        except: pass
        finally: client_socket.close()

    def start_listener(self, port):
        while True:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                server.bind((HOST, port))
                server.listen(500)
                while True:
                    client, addr = server.accept()
                    threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
            except: time.sleep(10)

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        print(f"[🚀] {VERSION} IS LIVE. THE INVISIBLE WALL IS STANDING.")
        while True: time.sleep(1)

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
