import asyncio
import os
import random
from datetime import datetime
from collections import defaultdict

# --- CONFIGURACIÓN ---
PORT_VOID = 6666
MAX_CONNECTIONS_PER_IP = 50
STICKY_INTERVAL_MIN = 10
STICKY_INTERVAL_MAX = 30
FIFIELD_BOMB_PATH = "/root/Active-Defense-Hell/assets/bombs/fifield_10G.bin.gz"
LOG_FILE = "/root/Active-Defense-Hell/logs/lucifer_prime.log"

ip_connection_tracker = defaultdict(int)

def log_lucifer(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{ts}] {msg}
"
    with open(LOG_FILE, "a") as f:
        f.write(entry)
    print(entry.strip())

async def handle_client(reader, writer):
    peer_addr = writer.get_extra_info('peername')
    if not peer_addr:
        writer.close()
        return
    ip = peer_addr[0]
    
    # Auto-Exhaustion
    if ip_connection_tracker[ip] >= MAX_CONNECTIONS_PER_IP:
        writer.close()
        return

    ip_connection_tracker[ip] += 1
    log_lucifer(f"VOID_ENTRY: {ip} | Total: {ip_connection_tracker[ip]}")

    async def sticky_task():
        """Mantiene la conexión viva enviando bytes nulos periódicamente"""
        try:
            while not writer.is_closing():
                await asyncio.sleep(random.randint(STICKY_INTERVAL_MIN, STICKY_INTERVAL_MAX))
                writer.write(b'\x00')
                await writer.drain()
        except: pass

    st_task = asyncio.create_task(sticky_task())

    try:
        # Detectar protocolo (Timeout de 5s para no bloquear)
        try:
            data = await asyncio.wait_for(reader.read(1024), timeout=5)
        except asyncio.TimeoutError:
            data = None

        if data:
            payload = data.decode('utf-8', errors='ignore')
            # Si es HTTP, responder con el banner de MexCapital
            if any(k in payload for k in ['GET ', 'POST ', 'SEARCH']):
                log_lucifer(f"HTTP_HIT: {ip} | Triggering Deception")
                banner = "HTTP/1.1 200 OK
Content-Type: text/html
Server: MexCapital-Admin-v4

"
                writer.write(banner.encode())
                await writer.drain()

                # INYECCIÓN FIFIELD EN CHUNKS (SEGURO PARA RAM)
                if os.path.exists(FIFIELD_BOMB_PATH):
                    log_lucifer(f"💣 BOMB_DEPLOYED: {ip} | Injecting 10GB Payload")
                    with open(FIFIELD_BOMB_PATH, "rb") as f:
                        while chunk := f.read(64 * 1024): # 64KB Chunks
                            writer.write(chunk)
                            await writer.drain()
                            # Drip-feed para saturar el socket del atacante
                            await asyncio.sleep(0.01)
                else:
                    writer.write(b"<h1>MexCapital Security Gateway</h1>")
                    await writer.drain()
            else:
                log_lucifer(f"DARK_MODE: {ip} | Binary/Silent engagement")
        
        # Mantener al bot atrapado indefinidamente
        while not writer.is_closing():
            await asyncio.sleep(10)

    except Exception as e:
        log_lucifer(f"SESSION_ERROR: {ip} | {e}")
    finally:
        st_task.cancel()
        ip_connection_tracker[ip] -= 1
        try:
            writer.close()
            await writer.wait_closed()
        except: pass

async def main():
    if not os.path.exists(os.path.dirname(LOG_FILE)):
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    server = await asyncio.start_server(handle_client, '0.0.0.0', PORT_VOID)
    log_lucifer(f"LUCIFER_PRIME v2 ONLINE on port {PORT_VOID}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
