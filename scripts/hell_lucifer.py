import asyncio
import os
import time
import socket
import struct
import random
import binascii

# HELL-LUCIFER v1.2
# Dedicated Mini-Log & Payload Capture (Range: 20101-65535)

LUCIFER_PORT = 6666
MAIN_LOG = "logs/hell_activity.log"
MINI_LOG = "logs/lucifer_mini.log"
SO_ORIGINAL_DST = 80 

async def get_original_dst(writer):
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
    
    # 1. CAPTURA DE PAYLOAD (Primeros 1024 bytes)
    payload_hex = "NO_DATA"
    try:
        # Esperamos un máximo de 2 segundos para ver si el bot envía algo
        data = await asyncio.wait_for(reader.read(1024), timeout=2.0)
        if data:
            payload_hex = binascii.hexlify(data).decode('utf-8')
    except asyncio.TimeoutError:
        pass
    except:
        payload_hex = "ERROR_READING"

    # 2. REGISTRO EN MINI-LOG (Forense Rápido)
    mini_report = f"[{timestamp}] IP:{ip} | PORT:{original_port} | PAYLOAD:{payload_hex}\n"
    
    # 3. REGISTRO EN LOG PRINCIPAL (Visibilidad)
    main_report = f"\n[🔱 HELL-LUCIFER]: {timestamp}\n----------------------------------------\nIP: {ip}\nTarget Port: {original_port} (VOID RANGE)\nPayload Captured: {payload_hex[:64]}...\nAction: TRAPPED IN THE ABYSS\n----------------------------------------\n"
    
    try:
        with open(MINI_LOG, "a", encoding='utf-8') as f:
            f.write(mini_report)
        with open(MAIN_LOG, "a", encoding='utf-8') as f:
            f.write(main_report)
    except:
        pass

    try:
        # Tarpit Infinito
        while True:
            writer.write(os.urandom(512))
            await writer.drain()
            await asyncio.sleep(random.uniform(15, 45))
    except:
        pass
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass

async def main():
    print(f"[*] HELL-LUCIFER v1.2: Initializing Payload Capture on port {LUCIFER_PORT}...")
    try:
        server = await asyncio.start_server(handle_lucifer_engagement, '0.0.0.0', LUCIFER_PORT)
        async with server:
            await server.serve_forever()
    except Exception as e:
        print(f"[!] Critical Error in Lucifer: {e}")

if __name__ == "__main__":
    asyncio.run(main())
