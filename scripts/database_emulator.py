import time
import os
import random

def handle_mysql_trap(client_socket):
    """Simulación de MySQL 8.0 con rastreo de bytes"""
    total_bytes = 0
    try:
        # Handshake
        handshake = b"\x4a\x00\x00\x00\x0a\x38\x2e\x30\x2e\x32\x38\x00\x08\x00\x00\x00\x50\x7a\x6b\x53\x43\x43\x5a\x37\x00\xff\xf7\x08\x02\x00\xff\xc1\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x4d\x46\x34\x33\x30\x67\x4c\x32\x34\x4c\x00\x6d\x79\x73\x71\x6c\x5f\x6e\x61\x74\x69\x76\x65\x5f\x70\x61\x73\x73\x77\x6f\x72\x64\x00"
        client_socket.send(handshake)
        total_bytes += len(handshake)
        client_socket.recv(1024)
        client_socket.send(b"\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00")
        
        while True:
            data = client_socket.recv(1024)
            if not data: break
            if b"SHOW" in data.upper() or b"SELECT" in data.upper():
                msg = b"DATABASE: monex_prod_mx_2026\nTABLE: customer_vault\n"
                client_socket.send(msg)
                total_bytes += len(msg)
                
                # Stream de 100,000 filas (~15MB de datos)
                for i in range(100000):
                    fake_row = f"ID:{i}|CARD:4532-{random.randint(1000,9999)}-{random.randint(1000,9999)}|CVV:{random.randint(100,999)}\n".encode()
                    client_socket.send(fake_row)
                    total_bytes += len(fake_row)
                    if i % 1000 == 0: time.sleep(0.01)
            else:
                client_socket.send(b"OK\n")
    except: pass
    return total_bytes

def handle_mssql_trap(client_socket):
    total_bytes = 0
    try:
        client_socket.send(b"\x04\x01\x00\x25\x00\x00\x01\x00\x00\x00\x15\x00\x06\x01\x00\x1b\x00\x01\x02\x00\x1c\x00\x01\x03\x00\x1d\x00\x00\xff\x0a\x00\x0a\xd1\x00\x00")
        time.sleep(1)
        banner = b"Welcome to Microsoft SQL Server 2019\n"
        client_socket.send(banner)
        total_bytes += len(banner)
        while True:
            chunk = os.urandom(4096)
            client_socket.send(chunk)
            total_bytes += len(chunk)
            time.sleep(0.1)
    except: pass
    return total_bytes
