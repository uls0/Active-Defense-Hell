import time
import os
import random
from scripts import network_simulator

def terminal_crusher(client_socket):
    ansi_bomb = b"\x1b[2J\x1b[H\x1b[?1049h"
    try:
        while True:
            payload = ansi_bomb
            for _ in range(15):
                color = os.urandom(1)[0]
                payload += f"\x1b[48;5;{color}m".encode() + b"\x00" * 150000 + b"\a"
            client_socket.send(payload)
            time.sleep(0.04)
    except: pass

def handle_cowrie_trap(client_socket, ip, hit_count=0):
    try:
        prompt = b"root@hell-node-01:~# "
        client_socket.send(b"Welcome to Ubuntu 22.04.3 LTS\r\n")
        client_socket.send(prompt)

        while True:
            cmd = client_socket.recv(1024).decode().strip()
            if not cmd: break
            
            # --- DETECCIÓN DE MOVIMIENTO LATERAL ---
            if "ssh" in cmd or "ping" in cmd or "nmap" in cmd:
                # Extraer una IP falsa de la red interna
                fake_target = "10.0.0." + str(random.randint(2, 254))
                network_simulator.handle_lateral_request(client_socket, fake_target)
                return

            if len(cmd) > 0:
                client_socket.send(f"{cmd}: command not found\r\n".encode())
                client_socket.send(prompt)
    except: pass
