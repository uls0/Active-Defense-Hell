import asyncio
import os
import time
import socket
import struct
import random

# HELL-LUCIFER v1.0
# Omnipresence Capture Module (Range: 20101-65535)
# Redirected via Iptables to local port 6666

LUCIFER_PORT = 6666
LOG_FILE = "logs/hell_activity.log"
SO_ORIGINAL_DST = 80 # Constante para Linux para obtener el puerto original

async def get_original_dst(writer):
    """Extrae el puerto original antes de la redirección de iptables"""
    try:
        sock = writer.get_extra_info('socket')
        odst = sock.getsockopt(socket.SOL_IP, SO_ORIGINAL_DST, 16)
        _, port, _ = struct.unpack("!HH4s8s", odst)
        return port
    except:
        return "UNKNOWN"

async def handle_lucifer_engagement(reader, writer):
    addr = writer.get_extra_info('peername')
    ip = addr[0]
    original_port = await get_original_dst(writer)
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Registro en el log central de HELL
    report = f"
[🔱 HELL-LUCIFER]: {timestamp}
"
    report += f"----------------------------------------
"
    report += f"IP: {ip}
"
    report += f"Target Port: {original_port} (VOID RANGE)
"
    report += f"Action: TRAPPED IN THE ABYSS
"
    report += f"Mode: ASYNC-LETHAL-STALL
"
    report += f"----------------------------------------
"
    
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(report)

    try:
        # Tarpit Infinito: Envío de entropía cada 15-45 segundos
        while True:
            # Generamos 512 bytes de basura aleatoria para mantener el buffer lleno
            writer.write(os.urandom(512))
            await writer.drain()
            await asyncio.sleep(random.uniform(15, 45))
    except (ConnectionResetError, BrokenPipeError, Exception):
        pass
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    print(f"[*] HELL-LUCIFER: Initializing Void Watcher on port {LUCIFER_PORT}...")
    server = await asyncio.start_server(handle_lucifer_engagement, '0.0.0.0', LUCIFER_PORT)
    
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
