import random
import time

def handle_lateral_request(client_socket, target_ip):
    """Simula el acceso a una subred interna protegida por Zero-Trust"""
    print(f"[🛡️] ZERO-TRUST: Atacante intentando movimiento lateral hacia {target_ip}")
    
    internal_nodes = {
        "10.0.0.5": "vCenter-Mexico-Primary",
        "10.0.0.10": "DC-Secondary-Backup",
        "10.0.0.50": "Monex-SWIFT-Gateway"
    }
    node_name = internal_nodes.get(target_ip, "Internal-Generic-Server")
    
    try:
        msg = f"""
--- DIGITAL TV GROUP ZERO-TRUST GATEWAY ---
Target: {node_name} ({target_ip})
MFA Required. Please enter 6-digit Mobile Token: """
        client_socket.send(msg.encode())
        
        # El atacante escribirá algo, pero nunca será correcto
        client_socket.send(b"\n[!] MFA Token Timeout. Retrying authentication loop...\n")
        
        while True:
            client_socket.send(b"Waiting for MFA push notification approval...\n")
            time.sleep(60)
    except: pass
