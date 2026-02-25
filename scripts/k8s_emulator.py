import json
import random
import os
import time

def handle_k8s_request(path):
    """Genera respuestas realistas de la API de Kubernetes"""
    if "/api/v1/secrets" in path:
        # Secreto tentador: Certificado TLS del Core Banking
        return {
            "kind": "SecretList",
            "apiVersion": "v1",
            "metadata": {"selfLink": "/api/v1/secrets"},
            "items": [{
                "metadata": {"name": "mex-prod-tls-cert"},
                "data": {"tls.key": "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tL...[TRUNCATED]"}
            }]
        }
    
    if "/api/v1/pods" in path:
        return {
            "kind": "PodList",
            "items": [{"metadata": {"name": f"pod-finance-{random.randint(100,999)}"}}]
        }
    
    return {"kind": "Status", "status": "Forbidden", "message": "User anonymous cannot access this resource"}

def serve_backup_trap(client_socket):
    """Sirve un falso respaldo de DB mediante Drip-Feed"""
    print("[🍯] Atacante mordió el anzuelo en /home/Desktop/backup_DB")
    header = """HTTP/1.1 200 OK
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="backup_prod_2026.sql.gz"

"""
    client_socket.send(header.encode())
    
    # Enviar 1GB de datos goteando
    for _ in range(1024): # 1024 bloques de 1MB
        chunk = os.urandom(1024 * 1024)
        client_socket.send(chunk)
        time.sleep(random.uniform(1, 5)) # Retraso letal
    return True
