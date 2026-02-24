import os
import time
import random
import binascii

def smb_compression_bomb(client_socket):
    """
    Simula una cabecera de compresión SMB3 (SMB2 Compression Transform Header)
    indicando un tamaño original masivo para provocar agotamiento de memoria (OOM)
    en el parser del atacante (ej. Impacket o Nmap scripts).
    """
    # ProtocolId: \xfcSMB
    # OriginalCompressedSegmentSize: 0xffffffff (4GB)
    # CompressionAlgorithm: 1 (LZ77)
    # Payload corrupto.
    bomb = b"\xfcSMB" + b"\xff\xff\xff\x7f" + b"\x01\x00" + b"\x00\x00" + b"\x00\x00\x00\x00" + os.urandom(1024)
    client_socket.send(bomb)
    # Mantenemos el flujo para que el motor siga intentando descomprimir
    while True:
        client_socket.send(os.urandom(4096))
        time.sleep(0.05)

def smb_infinite_maze(client_socket):
    """
    Finge ser un listado infinito de carpetas (Share Enumeration).
    Envía constantemente estructuras de respuesta SMB truncadas.
    """
    header = binascii.unhexlify("fe534d4240000000000000000000000000000000000000000000000000000000")
    while True:
        # Falsos nombres de carpetas atractivos
        fake_shares = [b"NOMINA_2026", b"BACKUPS_DC", b"SYSVOL", b"NETLOGON", b"CONFIDENCIAL"]
        payload = header + random.choice(fake_shares) + os.urandom(64)
        client_socket.send(payload)
        time.sleep(0.5)

def smb_ntlm_blackhole(client_socket):
    """
    Atrapa herramientas de fuerza bruta NTLM (como CrackMapExec o Responder)
    iniciando un handshake y luego enviando el desafío a 1 byte por minuto.
    """
    # Cabecera SMB2 NEGOTIATE Response simulada
    challenge_header = binascii.unhexlify("fe534d4240000000160000000000000000000000000000000000000000000000")
    client_socket.send(challenge_header)
    while True:
        # Drip-feed extremo
        client_socket.send(b"\x00")
        time.sleep(30)

def handle_smb_attack(client_socket, ip, log_event_func, local_port):
    traps = [
        ("SMB Compression Bomb (Memory Exhaustion)", smb_compression_bomb),
        ("Infinite Share Maze (Crawler Trap)", smb_infinite_maze),
        ("NTLM Blackhole (Thread Kidnapping)", smb_ntlm_blackhole)
    ]
    trap_name, trap_func = random.choice(traps)
    log_event_func(ip, local_port, "SMB Active Defense", b"", status=f"Engaged: {trap_name}")
    try:
        trap_func(client_socket)
    except:
        pass
