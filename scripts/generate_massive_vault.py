import os
import random
import hashlib
import string

BASE_VAULT = "/root/Active-Defense-Hell/assets/poison_vault"
BOMB_PATH = "/root/Active-Defense-Hell/assets/bombs/fifield_10G.bin.gz"

# Configuración del Laberinto
ROOT_FOLDERS = 100
SUBFOLDERS_PER_ROOT = 50
FILES_PER_FOLDER = 20

FINANCIAL_WORDS = ["ledger", "transaction", "client_pii", "swift_code", "vault_access", "payroll", "audit", "tax_return", "compliance", "credit_score"]

def get_random_name():
    word = random.choice(FINANCIAL_WORDS)
    rand_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{word}_{rand_id}"

def generate_massive_tree():
    print(f"[*] Iniciando construcción de laberinto en {BASE_VAULT}...")
    if not os.path.exists(BASE_VAULT):
        os.makedirs(BASE_VAULT, exist_ok=True)

    for i in range(ROOT_FOLDERS):
        root_path = os.path.join(BASE_VAULT, f"MEXCAPITAL_DB_NODE_{i:03d}")
        os.makedirs(root_path, exist_ok=True)
        
        for j in range(SUBFOLDERS_PER_ROOT):
            sub_name = get_random_name()
            sub_path = os.path.join(root_path, sub_name)
            os.makedirs(sub_path, exist_ok=True)
            
            # Crear archivos en la subcarpeta
            for k in range(FILES_PER_FOLDER):
                file_name = f"{get_random_name()}.dat"
                with open(os.path.join(sub_path, file_name), "w") as f:
                    # Generar 1KB de Hexadecimales aleatorios
                    f.write(os.urandom(512).hex())
            
            # Cada 25 subcarpetas, inyectar una Bomba Fifield oculta
            if j % 25 == 0:
                bomb_link = os.path.join(sub_path, "FULL_ENCRYPTED_BACKUP.zip")
                if os.path.exists(BOMB_PATH):
                    if os.path.exists(bomb_link): os.remove(bomb_link)
                    os.symlink(BOMB_PATH, bomb_link)

    print(f"[✔] Laberinto completado: {ROOT_FOLDERS * SUBFOLDERS_PER_ROOT} carpetas y {ROOT_FOLDERS * SUBFOLDERS_PER_ROOT * FILES_PER_FOLDER} archivos creados.")

if __name__ == "__main__":
    generate_massive_tree()
