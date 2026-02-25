import os
import time
import random
import binascii

def smb_compression_bomb(client_socket, tracker):
    # Header: 16 bytes
    bomb_header = b"\xfcSMB" + b"\xff\xff\xff\x7f" + b"\x01\x00" + b"\x00\x00" + b"\x00\x00\x00\x00"
    client_socket.send(bomb_header)
    tracker['bytes'] += len(bomb_header)
    
    while True:
        chunk = os.urandom(4096)
        client_socket.send(chunk)
        tracker['bytes'] += len(chunk)
        time.sleep(0.05)

def smb_infinite_maze(client_socket, tracker):
    header = binascii.unhexlify("fe534d4240000000000000000000000000000000000000000000000000000000")
    while True:
        fake_shares = [b"NOMINA_2026", b"BACKUPS_DC", b"SYSVOL", b"NETLOGON"]
        payload = header + random.choice(fake_shares) + os.urandom(64)
        client_socket.send(payload)
        tracker['bytes'] += len(payload)
        time.sleep(0.5)

def smb_ntlm_blackhole(client_socket, tracker):
    challenge_header = binascii.unhexlify("fe534d4240000000160000000000000000000000000000000000000000000000")
    client_socket.send(challenge_header)
    tracker['bytes'] += len(challenge_header)
    while True:
        client_socket.send(b"\x00")
        tracker['bytes'] += 1
        time.sleep(30)

def handle_smb_attack(client_socket, ip, log_event_func, local_port):
    tracker = {'bytes': 0}
    traps = [
        ("SMB Compression Bomb", smb_compression_bomb),
        ("Infinite Share Maze", smb_infinite_maze),
        ("NTLM Blackhole", smb_ntlm_blackhole)
    ]
    trap_name, trap_func = random.choice(traps)
    print(f"[⚔] Engaged {trap_name} against {ip}")
    try:
        trap_func(client_socket, tracker)
    except:
        pass
    return tracker['bytes']
