import socket
import ssl
import json
import time
import random
import os
import threading
import base64

# Configuración MexCapital
MEX_ORG = "MexCapital Servicios Financieros S.A. de C.V."
CERT_PATH = "assets/certs/mexcapital.crt"
KEY_PATH = "assets/certs/mexcapital.key"
BOMB_PATH = "assets/bombs/fifield_10G.bin.gz"
LOOT_FILE = "logs/credentials.log"

class EliteHandler:
    def __init__(self, log_func):
        self.log_event = log_func
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        if os.path.exists(CERT_PATH) and os.path.exists(KEY_PATH):
            self.ssl_context.load_cert_chain(certfile=CERT_PATH, keyfile=KEY_PATH)

    def log_loot(self, ip, port, user, password):
        ts = time.strftime('%H:%M:%S')
        entry = f"[{ts}] IP:{ip} | PORT:{port} | LOOT: {user}:{password}\n"
        with open(LOOT_FILE, "a") as f: f.write(entry)
        self.log_event(ip, port, "💎 LOOT_CAPTURED", f"{user}:{password}")

    def inject_fifield_bomb(self, client_socket, ip, port):
        self.log_event(ip, port, "💣 LETHAL_INJECTION", "FIFIELD_10GB_ACTIVE")
        try:
            if os.path.exists(BOMB_PATH):
                with open(BOMB_PATH, "rb") as f:
                    while chunk := f.read(1024 * 64):
                        client_socket.sendall(chunk)
                        time.sleep(0.01)
            else:
                client_socket.sendall(b"0" * 1024 * 1024 * 100)
        except: pass
        finally: client_socket.close()

    def handle_k8s(self, client_socket, ip, port):
        time.sleep(random.uniform(0.1, 0.5))
        response = {
            "kind": "PodList", "apiVersion": "v1",
            "items": [{"metadata": {"name": f"mex-fin-prod-{random.randint(100,999)}"}, "status": {"phase": "Running"}}]
        }
        headers = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nServer: MexCapital-K8s-Gateway\r\n\r\n"
        client_socket.sendall((headers + json.dumps(response)).encode())
        self.inject_fifield_bomb(client_socket, ip, port)

    def handle_docker(self, client_socket, ip, port):
        response = [{"Names": ["/mex-crypto-miner"], "Image": "mexcapital/internal:v2.1", "State": "running"}]
        headers = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nServer: Docker/19.03.12 (linux)\r\n\r\n"
        client_socket.sendall((headers + json.dumps(response)).encode())
        self.inject_fifield_bomb(client_socket, ip, port)

    def handle_prometheus(self, client_socket, ip, port):
        metrics = "# HELP mex_capital_tx_count Total financial transactions\nmex_capital_tx_count 99432\n"
        headers = "HTTP/1.1 200 OK\r\nContent-Type: text/plain; version=0.0.4\r\n\r\n"
        client_socket.sendall((headers + metrics).encode())
        client_socket.close()

    def handle_elastic(self, client_socket, ip, port):
        response = {"name" : "mex-fin-es-01", "cluster_name" : "mex-prod-cluster", "version" : {"number" : "7.10.0"}}
        headers = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
        client_socket.sendall((headers + json.dumps(response)).encode())
        self.inject_fifield_bomb(client_socket, ip, port)

    def handle_redis(self, client_socket, ip, port):
        try:
            data = client_socket.recv(1024).decode('utf-8', errors='ignore').upper()
            if "AUTH" in data:
                parts = data.split()
                user = "redis_user"
                password = parts[1] if len(parts) > 1 else "NO_PASS"
                self.log_loot(ip, port, user, password)
                client_socket.sendall(b"+OK\r\n")
            elif "PING" in data: client_socket.sendall(b"+PONG\r\n")
            elif "GET" in data:
                val = f"$64\r\nmex_sess_{os.urandom(24).hex()}\r\n"
                client_socket.sendall(val.encode())
            else: client_socket.sendall(b"-ERR Unknown command\r\n")
        except: pass
        finally: client_socket.close()

    def handle_shadow_api(self, client_socket, ip, port):
        try:
            data = client_socket.recv(1024).decode('utf-8', errors='ignore')
            if "Authorization: Basic" in data:
                try:
                    auth_val = data.split("Authorization: Basic ")[1].split("\r\n")[0]
                    creds = base64.b64decode(auth_val).decode('utf-8')
                    u, p = creds.split(":") if ":" in creds else (creds, "NONE")
                    self.log_loot(ip, port, u, p)
                except: pass
            
            response = {"status": "active", "api_version": "v1.0.4-LOCKED", "mex_auth_provider": "Internal-Oauth2"}
            headers = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nServer: Apache/2.4.49 (Unix)\r\n\r\n"
            client_socket.sendall((headers + json.dumps(response)).encode())
        except: pass
        self.inject_fifield_bomb(client_socket, ip, port)

    def handle_ai(self, client_socket, ip, port):
        response = {"id": f"mex-ai-{random.randint(1000,9999)}", "model": "mexcapital-fin-llama-3"}
        headers = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
        client_socket.sendall((headers + json.dumps(response)).encode())
        client_socket.close()

    def dispatch(self, client_socket, addr, port):
        ip = addr[0]
        self.log_event(ip, port, "🔥 ELITE_ENGAGEMENT", "MEXCAPITAL_BREADCRUMB_HIT")
        if port in [6443, 2376, 8081, 5000, 8000]:
            try:
                client_socket = self.ssl_context.wrap_socket(client_socket, server_side=True)
            except: client_socket.close(); return
        if port in [6443, 8080]: self.handle_k8s(client_socket, ip, port)
        elif port in [2375, 2376]: self.handle_docker(client_socket, ip, port)
        elif port in [9100, 9090]: self.handle_prometheus(client_socket, ip, port)
        elif port in [9200, 5601]: self.handle_elastic(client_socket, ip, port)
        elif port in [6379, 11211]: self.handle_redis(client_socket, ip, port)
        elif port in [8081, 3000, 5000]: self.handle_shadow_api(client_socket, ip, port)
        elif port in [8000, 11434]: self.handle_ai(client_socket, ip, port)
        else: client_socket.close()
