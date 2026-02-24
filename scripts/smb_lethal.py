import os
import time
import random
import binascii

def smb_compression_bomb(client_socket):
    sent = 0
    # Header: 16 bytes
    bomb_header = b"\xfcSMB" + b"\xff\xff\xff\x7f" + b"\x01\x00" + b"\x00\x00" + b"\x00\x00\x00\x00"
    client_socket.send(bomb_header)
    sent += len(bomb_header)
    
    while True:
        chunk = os.urandom(4096)
        client_socket.send(chunk)
        sent += len(chunk)
        time.sleep(0.05)
    return sent

def smb_infinite_maze(client_socket):
    sent = 0
    header = binascii.unhexlify("fe534d4240000000000000000000000000000000000000000000000000000000")
    while True:
        fake_shares = [b"NOMINA_2026", b"BACKUPS_DC", b"SYSVOL", b"NETLOGON"]
        payload = header + random.choice(fake_shares) + os.urandom(64)
        client_socket.send(payload)
        sent += len(payload)
        time.sleep(0.5)
    return sent

def smb_ntlm_blackhole(client_socket):
    sent = 0
    challenge_header = binascii.unhexlify("fe534d4240000000160000000000000000000000000000000000000000000000")
    client_socket.send(challenge_header)
    sent += len(challenge_header)
    while True:
        client_socket.send(b"\x00")
        sent += 1
        time.sleep(30)
    return sent

def handle_smb_attack(client_socket, ip, log_event_func, local_port):
    """Retorna el total de bytes enviados durante el ataque"""
    traps = [
        ("SMB Compression Bomb", smb_compression_bomb),
        ("Infinite Share Maze", smb_infinite_maze),
        ("NTLM Blackhole", smb_ntlm_blackhole)
    ]
    trap_name, trap_func = random.choice(traps)
    # Log de inicio del contraataque específico
    print(f"[⚔] Engaged {trap_name} against {ip}")
    try:
        return trap_func(client_socket)
    except:
        return 0
