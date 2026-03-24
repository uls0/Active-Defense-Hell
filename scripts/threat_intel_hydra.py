import os
import time, os, requests, json, socket

# --- CONFIGURACIÓN HYDRA ---
ABUSE_KEY = ""os.getenv('ABUSE_API_KEY')""
VT_KEY = ""os.getenv('VT_API_KEY')""
LOG_FILE = "/root/Active-Defense-Hell/logs/hell_activity.log"
PEER_IP = ""os.getenv('SEC_IP')"" # Cambiar segun nodo

def poke_back(ip, port):
    print(f"[🔥] INICIANDO POKE-BACK SWARM CONTRA {ip}...")
    # 1. Escaneo agresivo de banners (Saturación de logs del atacante)
    common_ports = [21, 22, 23, 80, 443, 445, 3306, 3389, 8080, 8443]
    for p in common_ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((ip, p))
            s.sendall(b"HELL_STORM_PROBE_v17.6
")
            s.close()
        except: pass

def report_swarm(ip, port):
    # Reporte a plataformas
    headers_vt = {"x-apikey": VT_KEY, "Content-Type": "application/json"}
    payload_vt = {"data": {"type": "comment", "attributes": {"text": f"HYDRA-MESH-DETECTION: Confirmed malicious node. Distributed capture by nodes PRO and SEC."}}}
    try: requests.post(f"https://www.virustotal.com/api/v3/ip_addresses/{ip}/comments", json=payload_vt, headers=headers_vt, timeout=5)
    except: pass
    
    # Notificar al Peer para que también haga Poke-Back
    try: requests.get(f"http://{PEER_IP}:8888/api/swarm_trigger?ip={ip}&port={port}", timeout=1)
    except: pass

# ... (Lógica de monitoreo de logs similar a la anterior) ...
