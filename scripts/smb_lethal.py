import time
import random
import socket
import os
import hashlib

# IP del servidor HELL para los canarios (pública)
HELL_IP = os.getenv("MY_IP", "178.128.72.149")

def generate_canary_url(ip, file_name):
    """Genera una URL canario única vinculada a la IP del bot."""
    token = hashlib.sha1(f"{ip}:{file_name}:{time.time()}".encode()).hexdigest()[:8]
    # El endpoint vive en el dashboard server (puerto 8888)
    return f"http://{HELL_IP}:8888/v1/auth/verify/{token}"

def handle_smb_session(client_socket, ip):
    """
    Simula un servidor SMB corporativo con Inyección de Canarios (v12.6-HUNT).
    """
    session_bytes = 0
    start_time = time.time()
    
    LURES = [
        "AWS_Root_Access_Keys_PROD.json", "CEO_Private_Email_Archive.pst", "Salary_Review_2026.xlsx",
        "MongoDB_Atlas_Admin_Auth.json", "VPN_Config_Keys.ovpn", "GitHub_Enterprise_Token.txt",
        "Azure_Global_Admin_Secret.txt", "Production_DB_Backup_Snapshot.sql"
    ]

    try:
        # 1. STALL INICIAL (3s)
        time.sleep(3.0)
        client_socket.send(b"\x00\x00\x00\x85\xffSMB\x72\x00\x00\x00\x00\x18\x53\xc8\x00\x00")
        
        # 2. GOTEO DE CARNADAS CON CANARIOS
        random.shuffle(LURES)
        
        for lure in LURES:
            try:
                time.sleep(random.uniform(0.5, 1.5))
                
                # Si el bot intenta leer el contenido del archivo
                # Generamos una URL de rastreo única para este evento
                canary_link = generate_canary_url(ip, lure)
                
                # Inyectamos el canario según el formato del archivo
                if ".json" in lure:
                    content = f'{{"access_key": "AKIA...", "secret": "...", "verify_internal": "{canary_link}"}}'
                elif ".txt" in lure or ".env" in lure:
                    content = f"ADMIN_TOKEN=ghp_... \nVERIFY_ENDPOINT={canary_link}\n"
                elif ".sql" in lure:
                    content = f"-- Master DB Credentials --\nINSERT INTO auth_keys VALUES ('admin', 'p@ss', '{canary_link}');\n"
                else:
                    content = f"Internal Verification Required: {canary_link}\n"
                
                # Enviamos metadatos de archivo
                fake_info = f"[FILE] {lure} | Content: {content}\n"
                client_socket.send(fake_info.encode())
                session_bytes += len(fake_info)
                
            except: break

        # 3. MANTENER CONEXIÓN (Infinite Tarpit)
        while True:
            if time.time() - start_time > 14400: break
            time.sleep(10)
            try:
                client_socket.send(b"\x00" * 512)
                session_bytes += 512
            except: break
                
    except Exception: pass
    return session_bytes
