import socket
import json
import time
import os
import subprocess

# CONFIGURACIÓN DEL NODO MESH v9.0.0
PORT = 9999
INTEL_FILE = "logs/mesh_intel.json"
NODE_ID = os.getenv("HELL_NODE_ID", "EXTERNAL-NODE-01")
PEERS = [p.strip() for p in os.getenv("HELL_MESH_PEERS", "").split(",") if p.strip()]

def block_at_kernel(ip):
    """Bloquea la IP permanentemente usando Iptables (Requiere Root)"""
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        print(f"[🛡️] THE WALL: IP {ip} bloqueada a nivel de Kernel.")
    except: pass

def listen_and_sync():
    os.makedirs("logs", exist_ok=True)
    if not os.path.exists(INTEL_FILE):
        with open(INTEL_FILE, 'w') as f: json.dump({"blacklist_ips": {}, "blacklist_ja3": {}, "peers_load": {}}, f)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(('0.0.0.0', PORT))
        print(f"[🌐] MESH CONTROLLER v9.0.0 ACTIVE")
        
        while True:
            data, addr = sock.recvfrom(4096)
            msg = json.loads(data.decode())
            
            # --- MANEJO DE ALERTAS DE AMENAZA ---
            if msg["type"] == "THREAT_ALERT":
                target = msg["target"]
                t_type = "blacklist_ips" if msg["target_type"] == "IP" else "blacklist_ja3"
                
                with open(INTEL_FILE, 'r+') as f:
                    intel = json.load(f)
                    intel[t_type][target] = {
                        "level": msg["level"],
                        "origin": msg["node_origin"],
                        "timestamp": msg["timestamp"]
                    }
                    f.seek(0); json.dump(intel, f, indent=4); f.truncate()
                
                # SI LA AMENAZA ES CRÍTICA, ACTIVAR EL MURO
                if msg["level"] == "CRITICAL" and msg["target_type"] == "IP":
                    block_at_kernel(target)

            # --- MANEJO DE CARGA (SWARMING) ---
            elif msg["type"] == "LOAD_UPDATE":
                with open(INTEL_FILE, 'r+') as f:
                    intel = json.load(f)
                    intel["peers_load"][msg["node_origin"]] = {
                        "ip": addr[0],
                        "load": msg["load"],
                        "last_seen": time.time()
                    }
                    f.seek(0); json.dump(intel, f, indent=4); f.truncate()

    except Exception as e:
        print(f"[!] Mesh Collector Error: {e}")

if __name__ == "__main__":
    listen_and_sync()
