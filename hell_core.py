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
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, mesh_node, predictive_ai

# CONFIGURACIÓN HELL v8.5.1: JA3 GLOBAL MESH REPUTATION
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
SCADA_PORTS = [502]
PORTS = WEB_PORTS + LETHAL_PORTS + SCADA_PORTS
LOG_FILE = "logs/hell_activity.log"

MESH_PEERS = os.getenv("HELL_MESH_PEERS", "").split(",") 
NODE_ID = os.getenv("HELL_NODE_ID", "NODE-SFO-01")

MY_IP = os.getenv("MY_IP", "127.0.0.1")

class HellServer:
    def __init__(self):
        os.makedirs("logs/malware", exist_ok=True)
        os.makedirs("logs/abuse_reports", exist_ok=True)
        self.whitelist = {MY_IP, "127.0.0.1"}
        self.stats = {} 
        self.mesh = mesh_node.start_mesh_service(NODE_ID, [p.strip() for p in MESH_PEERS if p.strip()])
        self.ai = predictive_ai.HellPredictiveAI()
        print(f"HELL CORE v8.5.1: JA3 Global Blacklisting Ready.")

    def log_engagement(self, ip, port, mesh_pre_flag=False, prediction_data=None, ja3=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        rdns, loc, asn, isp, profile = self.get_full_intel(ip)
        
        if ip not in self.stats: self.stats[ip] = {'hits': 1, 'total_time': 0, 'total_data': 0}
        else: self.stats[ip]['hits'] += 1

        prefix = "[📡 MESH-BLOCK]" if mesh_pre_flag else "[+] ULTIMATE DECEPTION"
        ai_tag = f" [🧠 PREDICTED: {prediction_data[0]}]" if prediction_data and prediction_data[0] else ""
        ja3_tag = f" [🛡️ JA3: {ja3}]" if ja3 else ""
        
        report = (
            f"\n{prefix} TRIGGERED: {timestamp}{ai_tag}{ja3_tag}\n"
            f"----------------------------------------\n"
            f"IP: {ip} ({rdns})\n"
            f"Origin: {loc} | Profile: {profile}\n"
            f"Network: {isp} ({asn})\n"
            f"Target Port: {port} | Hit Count: {self.stats[ip]['hits']}\n"
            f"----------------------------------------\n"
        )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(report)

    def get_full_intel(self, ip):
        try:
            try: rdns = socket.gethostbyaddr(ip)[0]
            except: rdns = ip
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp,proxy", timeout=3).json()
            loc = f"{r.get('city', 'Unknown')}, {r.get('country', 'Unknown')}"
            asn = r.get('as', 'Unknown ASN')
            isp = r.get('isp', 'Unknown ISP')
            profile = "PROXY/VPN" if r.get('proxy') else "DATACENTER/BOT"
            return rdns, loc, asn, isp, profile
        except: return ip, "Unknown", "Unknown", "Unknown", "Unknown"

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        ja3_hash = None
        # --- TLS FINGERPRINTING (JA3) ---
        if local_port in [443, 8443]:
            try:
                peek_data = client_socket.recv(1024, socket.MSG_PEEK)
                ja3_hash = ja3_engine.get_ja3_hash(peek_data)
            except: pass

        # --- MESH REPUTATION CHECK (IP + JA3) ---
        is_known, reason = self.mesh.check_reputation(ip, ja3_hash)
        if is_known:
            self.log_engagement(ip, local_port, mesh_pre_flag=True, ja3=ja3_hash)
            # Destrucción Inmediata si es conocido por el Mesh
            if local_port in [22, 2222]: shell_emulator.terminal_crusher(client_socket)
            else: zip_generator.serve_zip_trap(client_socket)
            return

        # AI Sequence Analysis
        predicted_port, confidence = self.ai.analyze_sequence(ip, local_port)

        start_time = time.time()
        final_mode = "Mitigation"
        total_bytes = 0

        threading.Thread(target=self.log_engagement, args=(ip, local_port, False, (predicted_port, confidence), ja3_hash)).start()

        try:
            client_socket.settimeout(10.0)
            data = client_socket.recv(4096)
            req_str = data.decode('utf-8', errors='ignore')

            if "/owa" in req_str or ".zip" in req_str or "GET / " in req_str:
                final_mode = "Fifield Ultra-Dense Attack"
                zip_generator.serve_zip_trap(client_socket)
                return
            
            if local_port == 22:
                final_mode = "Cowrie Login Trap"
                shell_emulator.handle_cowrie_trap(client_socket, ip)
                return
            
            if local_port == 2222:
                final_mode = "Mainframe Monex Simulation"
                shell_emulator.handle_mainframe_shell(client_socket, ip)
                return

            if local_port in SCADA_PORTS:
                final_mode = "SCADA Deception"
                scada_emulator.scada_tarpit(client_socket)
                return

            while True:
                client_socket.send(b"\x00")
                total_bytes += 1
                time.sleep(30)

        except: pass
        finally:
            duration = time.time() - start_time
            self.log_neutralization(ip, duration, total_bytes, final_mode, ja3_hash)
            try: client_socket.close()
            except: pass

    def log_neutralization(self, ip, duration, bytes_sent, mode, ja3=None):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        mb_sent = round(bytes_sent / (1024 * 1024), 4)
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
        
        # ANUNCIAR IP Y JA3 AL MESH
        if duration > 120 or mb_sent > 5:
            self.mesh.broadcast_threat(ip, "CRITICAL", mode, type="IP")
            if ja3:
                self.mesh.broadcast_threat(ja3, "CRITICAL", f"Tools used by {ip}", type="JA3")

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
        print(f"[✅] HELL CORE v8.5.1 (MESH-INTEL) desplegado.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    HellServer().start()
