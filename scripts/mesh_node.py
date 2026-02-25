import socket
import threading
import json
import time
import os

try:
    import psutil
except ImportError:
    psutil = None

class HellMeshNode:
    def __init__(self, node_id, port=9999, peers=None):
        self.node_id = node_id
        self.port = port
        self.peers = peers or []
        self.intel_file = "logs/mesh_intel.json"
        self.shared_intel = self.load_intel()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.load_avg = 0
        
    def load_intel(self):
        os.makedirs("logs", exist_ok=True)
        if os.path.exists(self.intel_file):
            with open(self.intel_file, 'r') as f:
                try: return json.load(f)
                except: pass
        return {"blacklist_ips": {}, "blacklist_ja3": {}, "peers_load": {}}

    def save_intel(self):
        with open(self.intel_file, 'w') as f:
            json.dump(self.shared_intel, f, indent=4)

    def broadcast_threat(self, target, level, details, target_type="IP"):
        message = {
            "node_origin": self.node_id,
            "type": "THREAT_ALERT",
            "target": target,
            "target_type": target_type,
            "level": level,
            "details": details,
            "timestamp": time.time()
        }
        data = json.dumps(message).encode()
        for peer in self.peers:
            try: self.sock.sendto(data, (peer, self.port))
            except: pass

    def listen_for_peers(self):
        try:
            self.sock.bind(('0.0.0.0', self.port))
            print(f"[🌐] MESH NODE ACTIVE on port {self.port}. Listening for peers...")
            while True:
                data, addr = self.sock.recvfrom(4096)
                msg = json.loads(data.decode())
                if msg["type"] == "THREAT_ALERT":
                    target = msg["target"]
                    list_key = "blacklist_ips" if msg["target_type"] == "IP" else "blacklist_ja3"
                    self.shared_intel[list_key][target] = {
                        "level": msg["level"],
                        "origin": msg["node_origin"],
                        "expires": msg["timestamp"] + 86400
                    }
                    self.save_intel()
                    print(f"[💉] Mesh Intel: Synced {msg['target_type']} {target}")
        except Exception as e:
            print(f"[!] Mesh Listener Error: {e}")

def start_mesh_service(node_id="NODE-01", peers=None):
    """Entry point to start the Mesh as a background thread if called from core"""
    node = HellMeshNode(node_id, peers=peers)
    t = threading.Thread(target=node.listen_for_peers, daemon=True)
    t.start()
    return node

if __name__ == "__main__":
    # If run directly as an external module
    NODE_ID = os.getenv("HELL_NODE_ID", "EXTERNAL-NODE")
    PEERS = os.getenv("HELL_MESH_PEERS", "").split(",")
    peers = [p.strip() for p in PEERS if p.strip()]
    node = HellMeshNode(NODE_ID, peers=peers)
    node.listen_for_peers()
