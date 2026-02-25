import time
import os
import random

def handle_mysql_trap(client_socket):
    """Simulación de MySQL 8.0 para atraer bots de filtración"""
    try:
        # 1. Handshake Inicial de MySQL
        # Protocol: 10, Version: 8.0.28, Auth: mysql_native_password
        handshake = (
            b"\x4a\x00\x00\x00\x0a\x38\x2e\x30\x2e\x32\x38\x00"
            b"\x08\x00\x00\x00\x50\x7a\x6b\x53\x43\x43\x5a\x37\x00"
            b"\xff\xf7\x08\x02\x00\xff\xc1\x15\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x4d\x46\x34\x33\x30\x67\x4c\x32\x34\x4c\x00"
            b"\x6d\x79\x73\x71\x6c\x5f\x6e\x61\x74\x69\x76\x65\x5f\x70\x61\x73\x73\x77\x6f\x72\x64\x00"
        )
        client_socket.send(handshake)
        
        # Recibir autenticación (Cualquier cosa sirve)
        client_socket.recv(1024)
        
        # 2. Responder OK al login
        client_socket.send(b"\x07\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00")
        
        # 3. Esperar comandos (Query)
        while True:
            data = client_socket.recv(1024)
            if b"SHOW DATABASES" in data.upper() or b"SELECT" in data.upper():
                # Iniciar la "Bomba de Datos"
                client_socket.send(b"DATABASE: monex_prod_mx_2026
TABLE: customer_vault_confidential
")
                client_socket.send(b"Starting Data Streaming...
")
                
                # Inundación de datos falsos (Drip-Feed)
                for i in range(1000000):
                    fake_row = f"ID:{i}|USER:user_{random.getrandbits(32)}|CARD:4532-{random.randint(1000,9999)}-{random.randint(1000,9999)}|CVV:{random.randint(100,999)}
"
                    client_socket.send(fake_row.encode())
                    if i % 100 == 0: time.sleep(0.01) # Tarpit suave para que el bot siga "bebiendo"
            else:
                client_socket.send(b"OK. Rows affected: 0")
    except: pass

def handle_mssql_trap(client_socket):
    """Simulación básica de SQL Server (TDS Protocol)"""
    try:
        # Pre-Login Response
        client_socket.send(b"\x04\x01\x00\x25\x00\x00\x01\x00\x00\x00\x15\x00\x06\x01\x00\x1b\x00\x01\x02\x00\x1c\x00\x01\x03\x00\x1d\x00\x00\xff\x0a\x00\x0a\xd1\x00\x00")
        time.sleep(1)
        # Login Acknowledgment + Infinite Stream
        client_socket.send(b"Welcome to Microsoft SQL Server 2019 (RTM) - 15.0.2000.5 (X64)
")
        while True:
            client_socket.send(os.urandom(4096))
            time.sleep(0.1)
    except: pass
