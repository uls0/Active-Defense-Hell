import os
import time
import random

def generate_fake_seed():
    """Genera una frase semilla falsa que actúa como carnada"""
    words = ["abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract", "absurd", "abuse", "access", "accident"]
    return " ".join(random.sample(words, 12))

def serve_honey_wallet(client_socket, filename):
    """Sirve archivos de carteras falsas usando Drip-Feed para amarrar al atacante"""
    print(f"[💰] Atacante intentando descargar Honey-Wallet: {filename}")
    
    if filename == "seed_phrase.txt":
        seed = generate_fake_seed()
        content = f"RECOVERY SEED FOR BTC WALLET (DO NOT SHARE):

{seed}

Balance: 14.52 BTC"
        header = f"HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: {len(content)}

"
        client_socket.send(header.encode() + content.encode())
        return "Seed Phrase Captured"

    # Para archivos grandes (wallet.dat), usamos Drip-Feed de 1GB
    header = f"HTTP/1.1 200 OK
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="{filename}"

"
    client_socket.send(header.encode())
    
    try:
        bytes_sent = 0
        while bytes_sent < 1024 * 1024 * 1024: # 1GB
            chunk = os.urandom(1024)
            client_socket.send(chunk)
            bytes_sent += len(chunk)
            time.sleep(random.uniform(0.1, 0.5)) # Retraso extremo
    except: pass
    return "Wallet Data Streamed"
