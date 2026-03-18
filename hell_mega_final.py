import os
import threading
import time
import socket
import sys
import json
import random
import requests

VERSION = "v14.2-FINAL-REBIRTH"
LOG_FILE = "logs/hell_activity.log"
HOST = '0.0.0.0'
PORTS = [22, 23, 80, 443, 445, 88, 135, 139, 179, 389, 449, 502, 102, 995, 1433, 2222, 2323, 3306, 3389, 4455, 8080, 8443, 9200, 33001, 1338, 8545, 3333, 18080, 32100, 14737, 37215, 52869, 38043, 50258, 20000, 47808, 6160]
PORTS.extend(range(20101, 20201))

class AdamServer:
    def __init__(self):
        print(f"[*] INITIALIZING MEGA-ADAM {VERSION}")
        if not os.path.exists("logs"): os.makedirs("logs")
        if not os.path.exists("payloads"): os.makedirs("payloads")

    def get_intel(self, ip):
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,as,isp", timeout=1.0).json()
            return f"{r.get('city')}, {r.get('country')}", r.get('as', 'Unknown')
        except: return "Unknown", "Unknown"

    def log_event(self, ip, port):
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        loc, asn = self.get_intel(ip)
        report = f"\n[ANGEL_DETECTED] {ts} | IP: {ip} | Port: {port} | Loc: {loc} | ASN: {asn}\n"
        with open(LOG_FILE, "a") as f: f.write(report)
        print(f"[+] Hit: {ip}:{port} ({loc})")

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        self.log_event(ip, local_port)
        try:
            client_socket.settimeout(5.0)
            if local_port == 3389:
                client_socket.recv(1024)
                client_socket.send(b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x12\x34\x00\x02\x01\x08\x00\x03\x00\x00\x00")
                time.sleep(0.5)
                client_socket.send(b"\x03\x00\x00\x6b\x02\xf0\x80\x7f\x66\x82\x00\x62\x0a\x01\x00\x02\x01\x00\x30\x5a\x02\x01\x21\x04\x01\x01\x04\x01\x01\x01\x01\xff")
                time.sleep(1); client_socket.close(); return
            if local_port in [80, 443, 8443, 8080]:
                res = "HTTP/1.1 200 OK\r\nServer: Microsoft-IIS/7.5\r\nContent-Type: text/html\r\n\r\n<h1>Restringido</h1>"
                client_socket.send(res.encode()); client_socket.close(); return
            if local_port == 445:
                client_socket.send(b"\x00\x00\x00\x85\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x18\x53\xc8\x00\x00")
                time.sleep(2); client_socket.close(); return
            client_socket.send(b"READY\n")
            while True:
                time.sleep(10); client_socket.send(b"\x00")
        except: pass
        finally: client_socket.close()

    def start_listener(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((HOST, port)); server.listen(100)
            while True:
                client, addr = server.accept()
                threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
        except: pass

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
            time.sleep(0.01)
        print(f"ADAM READY: {len(PORTS)} ports.")
        while True: time.sleep(1)

if __name__ == "__main__":
    AdamServer().start()
