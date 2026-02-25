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
from threat_intel import VirusTotalReporter, IsMaliciousReporter
from scripts import smb_lethal

# CONFIGURACIÓN HELL v5.0.0-ULTIMATE: DAMAGE ACCUMULATOR & DEEP FINGERPRINTING
HOST = '0.0.0.0'
WEB_PORTS = [80, 443, 8080, 8081, 8082, 8090, 8443, 9200]
LETHAL_PORTS = [22, 2222, 3389, 4455]
RAW_PORTS = [21, 23, 25, 445, 1433, 2323, 2525, 3306, 6379, 1337, 2375, 8125, 5060, 5900, 110, 5555]
AD_PORTS = [53, 88, 135, 389, 636, 3268, 5985]
AI_PORTS = [11434, 8188, 1234, 3000]
VULN_PORTS = [10443]

PORTS = WEB_PORTS + LETHAL_PORTS + RAW_PORTS + AD_PORTS + AI_PORTS + VULN_PORTS
LOG_FILE = "logs/hell_activity.log"

VT_KEY = os.getenv("VT_API_KEY", "")
ISM_KEY = "b0959d3e-97c6-451f-9f95-5148c2da7ddd"
ISM_SECRET = "643a5731-1af4-4632-b75c-65955138288a"
MY_IP = os.getenv("MY_IP", "127.0.0.1")

# Base de Datos de Daño Acumulado {ip: {"time": 0, "bytes": 0, "hits": 0}}
damage_stats = {}

class HellServer:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        self.vt_reporter = VirusTotalReporter(VT_KEY)
        self.ism_reporter = IsMaliciousReporter(ISM_KEY, ISM_SECRET)
        self.whitelist = {MY_IP, "127.0.0.1"}
        print(f"HELL CORE v5.0.0-ULTIMATE: All systems online. Accumulating threat damage.")

    def get_deep_intel(self, ip):
        """Consulta forense profunda y resolución inversa"""
        location, isp, profile, rdns = "Unknown", "Unknown", "Unknown", "N/A"
        try:
            # Resolución Inversa
            rdns = socket.gethostbyaddr(ip)[0]
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
        """Clasifica el tipo de bot basado en comportamiento"""
        d = data.decode('utf-8', errors='ignore').upper()
        if port in AD_PORTS: return "Active Directory Crawler"
        if port in AI_PORTS: return "AI Model Thief / Scraper"
        if port == 3389: return "RDP Brute-forcer / Ransomware"
        if "GET" in d or "POST" in d: return "Web Exploit Kit"
        if "SMB" in d or port == 445: return "SMB Worm / Lateral Movement"
        return "Generic Infrastructure Bot"

    def log_event(self, ip, local_port, scanner, status="START", intel=None, duration=0, bytes_sent=0, data=b""):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        if status == "START":
            loc, isp, prof, rdns = self.get_deep_intel(ip)
            bot_type = self.classify_bot(local_port, data)
            score = intel.get('score', 0) if intel else 0
            
            log_entry = (
                f"\n[+] ULTIMATE DECEPTION TRIGGERED: {timestamp}\n"
                f"----------------------------------------\n"
                f"IP: {ip} ({rdns})\n"
                f"Origin: {loc} | Profile: {prof}\n"
                f"Network: {isp}\n"
                f"Classification: {bot_type} | Score: {score}\n"
                f"Target Port: {local_port} | Hit Count: {damage_stats[ip]['hits']}\n"
            )
        else:
            mb_sent = round(bytes_sent / (1024 * 1024), 4)
            # Actualizar estadísticas acumuladas
            damage_stats[ip]["time"] += duration
            damage_stats[ip]["bytes"] += bytes_sent
            
            total_time = round(damage_stats[ip]["time"], 2)
            total_mb = round(damage_stats[ip]["bytes"] / (1024 * 1024), 2)
            
            log_entry = (
                f"[-] THREAT NEUTRALIZED: {timestamp}\n"
                f"    └─ Current Retention: {round(duration, 2)}s | Current Data: {mb_sent}MB\n"
                f"    └─ TOTAL DAMAGE: Time Lost: {total_time}s | Data Injected: {total_mb}MB\n"
                f"    └─ Final Mitigation: {status}\n"
                f"----------------------------------------\n"
            )
        with open(LOG_FILE, "a", encoding='utf-8') as f: f.write(log_entry)

    def anchored_send(self, client_socket, data):
        total = 0
        try:
            for i in range(0, len(data), random.randint(1, 10)):
                chunk = data[i:i+random.randint(1, 10)]
                client_socket.send(chunk)
                total += len(chunk)
                time.sleep(random.uniform(0.1, 0.4))
        except: pass
        return total

    def serve_zlib_bomb(self, client_socket):
        payload = b"\x00" * (1024 * 1024 * 100)
        compressed = zlib.compress(payload)
        header = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Encoding: deflate\r\n\r\n"
        client_socket.send(header.encode())
        return len(header) + self.anchored_send(client_socket, compressed)

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        if ip in self.whitelist:
            client_socket.close(); return

        if ip not in damage_stats:
            damage_stats[ip] = {"time": 0, "bytes": 0, "hits": 0}
        damage_stats[ip]["hits"] += 1
        
        start_time = time.time()
        total_bytes_sent = 0
        final_status = "Ultimate Retention"

        try:
            client_socket.settimeout(20.0)
            try: data = client_socket.recv(1024, socket.MSG_PEEK)
            except: data = b""

            intel = self.ism_reporter.check_ip(ip)
            self.log_event(ip, local_port, None, status="START", intel=intel, data=data)

            if local_port in AI_PORTS or local_port in WEB_PORTS:
                final_status = "Anchored Logic Bomb"
                total_bytes_sent += self.serve_zlib_bomb(client_socket)
            
            elif local_port in [22, 2222]:
                final_status = "Infinite SSH Tarpit"
                client_socket.send(b"SSH-2.0-OpenSSH_8.9p1\r\n")
                while True:
                    client_socket.send(os.urandom(1))
                    total_bytes_sent += 1
                    time.sleep(15)

            elif local_port == 3389:
                final_status = "RDP Bandwidth Murder"
                while True:
                    client_socket.send(os.urandom(65536))
                    total_bytes_sent += 65536
                    time.sleep(0.01)

            elif local_port == 445:
                final_status = "SMB Lethal Maze"
                total_bytes_sent += smb_lethal.handle_smb_attack(client_socket, ip, (lambda *args, **kwargs: None), local_port)
            
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
