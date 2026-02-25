import time
import os
import random
from scripts import network_simulator
try:
    from scripts import oracle_engine
except ImportError:
    oracle_engine = None

LOG_FILE = "logs/hell_activity.log"

def terminal_crusher(client_socket):
    ansi_bomb = b"\x1b[2J\x1b[H\x1b[?1049h"
    try:
        while True:
            payload = ansi_bomb
            for _ in range(15):
                color = os.random(1)[0] if hasattr(os, 'random') else random.randint(0,255)
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
            cmd_data = client_socket.recv(1024)
            if not cmd_data: break
            cmd = cmd_data.decode('utf-8', errors='ignore').strip()
            
            if not cmd:
                client_socket.send(prompt)
                continue

            if "ssh" in cmd or "ping" in cmd or "nmap" in cmd:
                fake_target = "10.0.0." + str(random.randint(2, 254))
                network_simulator.handle_lateral_request(client_socket, fake_target)
                return

            # --- ORACLE AI WITH MEMORY ---
            if oracle_engine and oracle_engine.oracle.enabled:
                ai_resp = oracle_engine.oracle.get_dynamic_response(ip, cmd)
                # Loggear interacción del Oráculo
                with open(LOG_FILE, "a") as f:
                    f.write(f"[🔮 ORACLE] IP {ip} executed '{cmd}' -> AI responded with {len(ai_resp)} bytes.\n")
                client_socket.send(f"{ai_resp}\r\n".encode())
            else:
                client_socket.send(f"{cmd}: command not found\r\n".encode())
            
            client_socket.send(prompt)
    except: pass
