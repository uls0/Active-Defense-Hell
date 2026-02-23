import socket
import threading
import time
import random
import os

# CONFIGURACIÓN DEL PROYECTO HELL
HOST = '0.0.0.0'
PORT = 8080
GZIP_BOMB_PATH = "payloads/bomb.gz"  # Se generará dinámicamente
WHITELIST_PATH = "whitelist.json"

class HellServer:
    def __init__(self):
        self.active_attackers = {}
        print("[💀] Proyecto HELL: Iniciando Sistema de Defensa Activa...")

    def generate_infinite_trash(self):
        """Genera basura aleatoria para el Infinite Stream (5MB/s aprox)"""
        while True:
            yield os.urandom(1024 * 1024) # 1MB de entropía pura

    def counter_attack(self, client_socket, addr, attack_type):
        """Lógica de contraataque basada en el comportamiento detectado"""
        if attack_type == "GZIP_BOMB":
            print(f"[🔥] LANZANDO GZIP BOMB contra {addr[0]}...")
            header = (
                "HTTP/1.1 200 OK
"
                "Content-Type: application/x-gzip
"
                "Content-Encoding: gzip
"
                "Content-Disposition: attachment; filename="backup_database.sql.gz"
"
                "
"
            )
            client_socket.send(header.encode())
            # Aquí enviaríamos el payload binario de la bomba
            
        elif attack_type == "INFINITE_STREAM":
            print(f"[🌊] INICIANDO INFINITE STREAM (5MB/s) contra {addr[0]}...")
            header = (
                "HTTP/1.1 200 OK
"
                "Transfer-Encoding: chunked
"
                "
"
            )
            client_socket.send(header.encode())
            try:
                for chunk in self.generate_infinite_trash():
                    size = hex(len(chunk))[2:]
                    client_socket.send(f"{size}
".encode() + chunk + b"
")
                    time.sleep(0.2) # Control de flujo para saturar sin morir nosotros
            except:
                print(f"[✔] Atacante {addr[0]} ha colapsado o cerrado la conexión.")

    def handle_client(self, client_socket, addr):
        try:
            request = client_socket.recv(2048).decode('utf-8', errors='ignore')
            
            # ANALÍTICA DE IA (Simulada para el Core inicial)
            if ".env" in request or "wp-config" in request:
                self.counter_attack(client_socket, addr, "INFINITE_STREAM")
            elif "backup" in request or "dump" in request:
                self.counter_attack(client_socket, addr, "GZIP_BOMB")
            else:
                client_socket.send("HTTP/1.1 404 Not Found

".encode())
                
        except Exception as e:
            print(f"[!] Error con {addr[0]}: {e}")
        finally:
            client_socket.close()

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(100)
        print(f"[✔] HELL Core escuchando en puerto {PORT} (Esperando intrusos...)")
        
        while True:
            client, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(client, addr)).start()

if __name__ == "__main__":
    # Asegurar carpetas base
    os.makedirs("payloads", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    hell = HellServer()
    hell.start()
