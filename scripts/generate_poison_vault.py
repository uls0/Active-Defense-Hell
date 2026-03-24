import os
import random
import hashlib

VAULT_DIR = "/root/Active-Defense-Hell/assets/poison_vault"
BOMB_PATH = "/root/Active-Defense-Hell/assets/bombs/fifield_10G.bin.gz"

def generate_vault():
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR, exist_ok=True)
    
    print(f"[*] Generando Poison Vault en {VAULT_DIR}...")

    # 1. Crear archivos de Confusión Financiera (Hashes sin sentido)
    filenames = [
        "mex_fin_ledger_2025.csv", "swift_transfers_batch_march.txt",
        "mex_capital_payroll_active.sql", "kyc_documents_audit.log"
    ]
    
    for name in filenames:
        with open(f"{VAULT_DIR}/{name}", "w") as f:
            for i in range(5000):
                fake_hash = hashlib.sha256(str(random.random()).encode()).hexdigest()
                f.write(f"TX_ID: {i} | HASH: {fake_hash} | STATUS: SUCCESS\n")
    
    # 2. Inyectar Placeholders para Canary Tokens
    with open(f"{VAULT_DIR}/INTERNAL_ACCESS_READ_ME.txt", "w") as f:
        f.write("CONFIDENTIAL: INTERNAL NETWORK ACCESS LOGS\nCANARY_URL_PLACEHOLDER\n")

    # 3. Vincular la Bomba Fifield
    targets = ["mex_capital_full_backup_2026.zip", "private_keys_donot_share.tar.gz"]
    if os.path.exists(BOMB_PATH):
        for target in targets:
            dest = f"{VAULT_DIR}/{target}"
            if os.path.exists(dest): os.remove(dest)
            os.symlink(BOMB_PATH, dest)
            print(f"[✔] Enlazando Bomba a: {target}")
    else:
        print("[!] Generando basura como fallback...")
        with open(f"{VAULT_DIR}/mex_capital_full_backup_2026.zip", "wb") as f:
            f.write(os.urandom(1024 * 1024 * 100))

    print("[✔] Vault listo.")

if __name__ == "__main__":
    generate_vault()
