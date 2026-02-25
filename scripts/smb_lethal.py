import os
import time
import random
import binascii

def smb_compression_bomb(client_socket, tracker):
    """Bomba de compresión SMB: Inunda el buffer del cliente"""
    bomb_header = b"\xfcSMB" + b"\xff\xff\xff\x7f" + b"\x01\x00" + b"\x00\x00" + b"\x00\x00\x00\x00"
    try:
        client_socket.send(bomb_header)
        tracker['bytes'] += len(bomb_header)
        while True:
            # Enviamos bloques de 1MB para saturación rápida
            chunk = os.urandom(1024 * 1024)
            client_socket.send(chunk)
            tracker['bytes'] += len(chunk)
            time.sleep(0.01)
    except: pass

def smb_infinite_maze(client_socket, tracker):
    """Laberinto infinito de carpetas AD"""
    header = binascii.unhexlify("fe534d4240000000000000000000000000000000000000000000000000000000")
    try:
        while True:
            fake_shares = [b"NOMINA_2026_MX", b"BACKUPS_DC_PRIMARY", b"SYSVOL_TVG", b"NETLOGON_CORP"]
            payload = header + random.choice(fake_shares) + b"\\" + os.urandom(32)
            client_socket.send(payload)
            tracker['bytes'] += len(payload)
            time.sleep(0.1)
    except: pass

def handle_smb_session(client_socket, ip):
    """Punto de entrada principal para el AD Falso"""
    tracker = {'bytes': 0}
    traps = [
        ("SMB Compression Bomb", smb_compression_bomb),
        ("Infinite Share Maze", smb_infinite_maze)
    ]
    trap_name, trap_func = random.choice(traps)
    
    # Este print será capturado por el log del CORE
    print(f"[🛡️] AD-FAKE: Iniciando {trap_name} contra {ip}")
    
    try:
        trap_func(client_socket, tracker)
    except: pass
    
    return tracker['bytes']
