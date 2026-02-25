import socket
import threading
import time
import os
import binascii
import random
import requests
import base64
import hashlib
import zlib
from datetime import datetime
from threat_intel import VirusTotalReporter, IsMaliciousReporter, AbuseIPDBReporter
from scripts import smb_lethal

# CONFIGURACIÓN HELL v5.1.0: GLOBAL THREAT REPORTING SYNC
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
RAW_PORTS = [21, 23, 25, 445, 1433, 2323, 2525, 3306, 6379, 1337, 2375, 8125, 5060, 5900, 110, 5555]
AD_PORTS = [53, 88, 135, 389, 636, 3268, 5985]
AI_PORTS = [11434, 8188, 1234, 3000]
VULN_PORTS = [10443]

PORTS = WEB_PORTS + LETHAL_PORTS + RAW_PORTS + AD_PORTS + AI_PORTS + VULN_PORTS
LOG_FILE = "logs/hell_activity.log"

# API KEYS
VT_KEY = os.getenv("VT_API_KEY", "")
ABUSE_KEY = os.getenv("ABUSEIPDB_API_KEY", "") # Obtén una gratis en abuseipdb.com
ISM_KEY = "b0959d3e-97c6-451f-9f95-5148c2da7ddd"
ISM_SECRET = "643a5731-1af4-4632-b75c-65955138288a"
MY_IP = os.getenv("MY_IP", "127.0.0.1")

damage_stats = {}

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.abuse_reporter = AbuseIPDBReporter(ABUSE_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v5.1.0: Global Reporting Sync Enabled (VT & AbuseIPDB).")

    def get_deep_intel(self, ip):
        location, isp, profile, rdns = "Unknown", "Unknown", "Unknown", "N/A"
        try: rdns = socket.gethostbyaddr(ip)[0]
        except: pass
        try:
            fields = "status,country,city,isp,as,proxy,hosting"
            r = requests.get(f"http://ip-api.com/json/{ip}?fields={fields}", timeout=3)
            if r.status_code == 200:
                d = r.json()
                location = f"{d.get('city')}, {d.get('country')}"
                isp = f"{d.get('isp')} ({d.get('as')})"
                p = []
                if d.get('proxy'): p.append("VPN/PROXY")
                if d.get('hosting'): p.append("DATACENTER")
                profile = " | ".join(p) if p else "RESIDENTIAL"
        except: pass
        return location, isp, profile, rdns

    def classify_bot(self, port, data):
        d = data.decode('utf-8', errors='ignore').upper()
        if port in AD_PORTS: return "Active Directory Crawler"
        if port in AI_PORTS: return "AI Model Thief"
        if port == 3389: return "RDP Brute-forcer"
        if "GET" in d or "POST" in d: return "Web Exploit Bot"
        return "Infrastructure Scanner"

    def log_event(self, ip, local_port, scanner, status="START", intel=None, duration=0, bytes_sent=0, data=b""):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if status == "START":
            loc, isp, prof, rdns = self.get_deep_intel(ip)
            bot_type = self.classify_bot(local_port, data)
            score = intel.get('score', 0) if intel else 0
            log_entry = (
                f"\n[+] ULTIMATE DECEPTION TRIGGERED: {timestamp}\n"
                f"----------------------------------------\n"
                f"IP: {ip} ({rdns}) | Port: {local_port}\n"
                f"Location: {loc} | Profile: {prof}\n"
                f"Network: {isp}\n"
                f"Classification: {bot_type} | Intel Score: {score}\n"
            )
            # Retornar datos forenses para el reporte asíncrono
            return {"location": loc, "isp": isp, "bot_type": bot_type}
        else:
            damage_stats[ip]["time"] += duration
            damage_stats[ip]["bytes"] += bytes_sent
            total_data = f"{round(damage_stats[ip]['bytes'] / (1024 * 1024), 2)} MB"
            log_entry = (
                f"[-] THREAT NEUTRALIZED: {timestamp}\n"
                f"    └─ TOTAL DAMAGE: Time: {round(damage_stats[ip]['time'], 2)}s | Data: {total_data}\n"
                f"    └─ Final Mitigation: {status}\n"
                f"----------------------------------------\n"
            )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        if ip not in damage_stats: damage_stats[ip] = {"time": 0, "bytes": 0, "hits": 0}
        damage_stats[ip]["hits"] += 1
        
        start_time = time.time()
        total_bytes_sent = 0
        final_status = "Ultimate Retention"

        try:
            client_socket.settimeout(15.0)
            try: data = client_socket.recv(1024, socket.MSG_PEEK)
            except: data = b""

            intel = self.ism_reporter.check_ip(ip)
            forensics = self.log_event(ip, local_port, None, status="START", intel=intel, data=data)

            # REPORTES GLOBALES ASÍNCRONOS (Cada 5 hits)
            if damage_stats[ip]["hits"] % 5 == 1:
                t1 = threading.Thread(target=self.vt_reporter.report_ip, 
                                     args=(ip, forensics['bot_type'], local_port, data, forensics['location'], forensics['isp']))
                t2 = threading.Thread(target=self.abuse_reporter.report_ip, 
                                     args=(ip, local_port, forensics['bot_type']))
                t1.start(); t2.start()

            # --- ESTRATEGIAS LETHAL ---
            if local_port in AI_PORTS or local_port in WEB_PORTS:
                final_status = "Anchored Logic Bomb"
                payload = b"\x00" * (1024 * 1024 * 50)
                compressed = zlib.compress(payload)
                header = "HTTP/1.1 200 OK\r\nContent-Encoding: deflate\r\n\r\n"
                client_socket.send(header.encode())
                for i in range(0, len(compressed), 5):
                    client_socket.send(compressed[i:i+5])
                    total_bytes_sent += 5
                    time.sleep(0.1)
            
            elif local_port in [22, 2222]:
                final_status = "Infinite SSH Tarpit"
                client_socket.send(b"SSH-2.0-OpenSSH_8.9p1\r\n")
                while True:
                    client_socket.send(os.urandom(1))
                    total_bytes_sent += 1
                    time.sleep(15)

            elif local_port == 445:
                final_status = "SMB Lethal Maze"
                total_bytes_sent = smb_lethal.handle_smb_attack(client_socket, ip, None, local_port)
            
            else:
                while True:
                    client_socket.send(os.urandom(1024))
                    total_bytes_sent += 1024
                    time.sleep(5)

        except: pass
        finally:
            duration = time.time() - start_time
            self.log_event(ip, local_port, None, status=final_status, duration=duration, bytes_sent=total_bytes_sent)
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
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    HellServer().start()
