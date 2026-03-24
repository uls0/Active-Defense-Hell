import asyncio
import os
import time
import socket
import struct
import random
import binascii

# =============================================================================
# HELL-LUCIFER v1.5 - THE VOID PORT CAPTURE
# =============================================================================
# Captura de puertos originales mediante SO_ORIGINAL_DST (Iptables REDIRECT)
# =============================================================================

LUCIFER_PORT = 6666
MAIN_LOG = "logs/hell_activity.log"
MINI_LOG = "logs/lucifer_mini.log"

# En Linux x86/ARM, SO_ORIGINAL_DST suele ser 80
SO_ORIGINAL_DST = 80

async def get_original_dst(writer):
    """
    Recupera el puerto de destino original antes de la redireccion de Iptables.
    """
    try:
        sock = writer.get_extra_info('socket')
        # Intentamos obtener la estructura sockaddr_in (16 bytes)
        odst = sock.getsockopt(socket.SOL_IP, SO_ORIGINAL_DST, 16)
        
        # Desempaquetado: family (H), port (H), addr (4s), padding (8s)
        # Usamos big-endian (!) para los datos de red
        _, port, _, _ = struct.unpack("!HH4s8s", odst)
        return port
    except Exception as e:
        # Fallback silencioso si no es una redireccion de Iptables
        return "UNKNOWN"

async def handle_lucifer_engagement(reader, writer):
    addr = writer.get_extra_info('peername')
    ip = addr[0]
    original_port = await get_original_dst(writer)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Captura rapida de payload para el mini-log
    payload_hex = "NO_DATA"
    try:
        data = await asyncio.wait_for(reader.read(512), timeout=1.5)
        if data:
            payload_hex = binascii.hexlify(data).decode('utf-8')
    except:
        pass

    # Registro en log principal con el puerto REAL
    status_msg = f"[🔱 HELL-LUCIFER] | IP: {ip} | Target Port: {original_port} (VOID RANGE) | Action: TRAPPED\n"
    mini_msg = f"[{timestamp}] IP:{ip} | PORT:{original_port} | PAYLOAD:{payload_hex}\n"
    
    try:
        with open(MAIN_LOG, "a", encoding='utf-8') as f:
            f.write(status_msg)
        with open(MINI_LOG, "a", encoding='utf-8') as f:
            f.write(mini_msg)
    except:
        pass

    # Tarpit L7: Enviar basura lenta para retener al atacante
    try:
        while True:
            # Enviamos un fragmento de basura cada 20-40 segundos
            writer.write(os.urandom(256))
            await writer.drain()
            await asyncio.sleep(random.uniform(20, 40))
    except:
        pass
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass

async def main():
    print(f"[*] HELL-LUCIFER v1.5: Monitoring Void on port {LUCIFER_PORT}...")
    try:
        server = await asyncio.start_server(handle_lucifer_engagement, '0.0.0.0', LUCIFER_PORT)
        async with server:
            await server.serve_forever()
    except Exception as e:
        print(f"[!] Critical error in Lucifer: {e}")

if __name__ == "__main__":
    asyncio.run(main())
