import time
import os
import random
from scripts import network_simulator
try:
    from scripts import oracle_engine
except ImportError:
    oracle_engine = None

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
            cmd_data = client_socket.recv(1024)
            if not cmd_data: break
            cmd = cmd_data.decode('utf-8', errors='ignore').strip()
            
            if "ssh" in cmd or "ping" in cmd or "nmap" in cmd:
                fake_target = "10.0.0." + str(random.randint(2, 254))
                network_simulator.handle_lateral_request(client_socket, fake_target)
                return

            if len(cmd) > 0:
                # --- ORACLE AI RESPONSE ---
                if oracle_engine and oracle_engine.oracle.enabled:
                    ai_resp = oracle_engine.oracle.get_dynamic_response(cmd)
                    client_socket.send(f"{ai_resp}\r\n".encode())
                else:
                    client_socket.send(f"{cmd}: command not found\r\n".encode())
                
                client_socket.send(prompt)
    except: pass
