import socket
import json
import time
import os

# CONFIGURACIÓN DEL NODO MESH EXTERNO
PORT = 9999
INTEL_FILE = "logs/mesh_intel.json"
NODE_ID = os.getenv("HELL_NODE_ID", "EXTERNAL-NODE-01")
PEERS = [p.strip() for p in os.getenv("HELL_MESH_PEERS", "").split(",") if p.strip()]

def listen_and_sync():
    os.makedirs("logs", exist_ok=True)
    if not os.path.exists(INTEL_FILE):
        with open(INTEL_FILE, 'w') as f: json.dump({"blacklist_ips": {}, "blacklist_ja3": {}}, f)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(('0.0.0.0', PORT))
        print(f"[🌐] MESH INTELLIGENCE COLLECTOR ACTIVE ON PORT {PORT}")
        print(f"[📡] Connected Peers: {PEERS}")
        
        while True:
            data, addr = sock.recvfrom(4096)
            msg = json.loads(data.decode())
            
            if msg["type"] == "THREAT_ALERT":
                target = msg["target"]
                t_type = "blacklist_ips" if msg["target_type"] == "IP" else "blacklist_ja3"
                
                # Cargar, actualizar y guardar
                with open(INTEL_FILE, 'r+') as f:
                    intel = json.load(f)
                    intel[t_type][target] = {
                        "level": msg["level"],
                        "origin": msg["node_origin"],
                        "timestamp": msg["timestamp"]
                    }
                    f.seek(0)
                    json.dump(intel, f, indent=4)
                    f.truncate()
                print(f"[💉] Intelligence Synced: {msg['target_type']} {target} from {msg['node_origin']}")
    except Exception as e:
        print(f"[!] Mesh Collector Error: {e}")

if __name__ == "__main__":
    listen_and_sync()
