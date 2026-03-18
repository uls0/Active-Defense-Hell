import os, threading, time, socket, sys, json, random, requests, zipfile, io

# =============================================================================
# PROJECT EVANGELION: MEGA-ADAM v15.0-IMMORTAL (THE FINAL CORE)
# =============================================================================

VERSION = "v15.0-IMMORTAL"
LOG_FILE = "/root/Active-Defense-Hell/logs/hell_activity.log"
HOST = '0.0.0.0'
PORTS = [22, 23, 80, 443, 445, 88, 135, 139, 179, 389, 449, 502, 102, 995, 1433, 2222, 2323, 3306, 3389, 4455, 8080, 8443, 9200, 33001, 1338, 8545, 3333, 18080, 32100, 14737, 37215, 52869, 38043, 50258, 20000, 47808, 6160]
PORTS.extend(range(20101, 20201))

class HellSystem:
    def __init__(self):
        print(f"[*] INITIALIZING MEGA-ADAM {VERSION}")
        os.makedirs("/root/Active-Defense-Hell/logs", exist_ok=True)
        self.stats = {}

    def log_event(self, ip, port, message="Hit"):
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        report = f"
[ANGEL_DETECTED] {ts} | IP: {ip} | Port: {port} | Action: {message}
"
        with open(LOG_FILE, "a") as f: f.write(report)
        print(f"[+] {message}: {ip}:{port}")

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
                res = "HTTP/1.1 200 OK
Server: Microsoft-IIS/7.5
Content-Type: text/html

<h1>Restringido</h1>"
                client_socket.send(res.encode()); client_socket.close(); return
            client_socket.send(b"READY
")
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

    # --- LUCIFER: EL VACIO (PORT 6666) ---
    def start_lucifer(self):
        print("[*] ACTIVATING LUCIFER (VOID) ON PORT 6666")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, 6666)); server.listen(1000)
        while True:
            client, addr = server.accept()
            ip = addr[0]
            self.log_event(ip, 6666, "TRAPPED IN THE ABYSS")
            client.close()

    # --- DASHBOARD: MINI-SERVER (PORT 8888) ---
    def start_dashboard(self):
        print("[*] ACTIVATING DASHBOARD ON PORT 8888")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, 8888)); server.listen(5)
        while True:
            client, addr = server.accept()
            try:
                data = client.recv(1024)
                with open(LOG_FILE, "r") as f: logs = f.readlines()[-20:]
                res = "HTTP/1.1 200 OK
Content-Type: text/plain

"
                res += "HELL v15.0 - DASHBOARD
" + "".join(logs)
                client.send(res.encode())
            except: pass
            finally: client.close()

    def start(self):
        threading.Thread(target=self.start_lucifer, daemon=True).start()
        threading.Thread(target=self.start_dashboard, daemon=True).start()
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
            time.sleep(0.01)
        print(f"[OK] ALL ANGELS ACTIVE. Vigilando {len(PORTS)} puertos.")
        while True: time.sleep(1)

if __name__ == "__main__":
    HellSystem().start()
