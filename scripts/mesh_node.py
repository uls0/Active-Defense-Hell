import socket
import threading
import json
import time
import os

class HellMeshNode:
    def __init__(self, node_id, port=9999, peers=None):
        self.node_id = node_id
        self.port = port
        self.peers = peers or []
        self.intel_file = "logs/mesh_intel.json"
        self.shared_intel = self.load_intel()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def load_intel(self):
        if os.path.exists(self.intel_file):
            with open(self.intel_file, 'r') as f:
                return json.load(f)
        return {"blacklist_ips": {}, "blacklist_ja3": {}, "honey_tokens": []}

    def save_intel(self):
        with open(self.intel_file, 'w') as f:
            json.dump(self.shared_intel, f, indent=4)

    def broadcast_threat(self, target, level, details, type="IP"):
        """Anuncia una IP o un JA3 Hash al Mesh"""
        message = {
            "node_origin": self.node_id,
            "type": "THREAT_ALERT",
            "target": target,
            "target_type": type, # "IP" o "JA3"
            "level": level,
            "details": details,
            "timestamp": time.time()
        }
        data = json.dumps(message).encode()
        for peer in self.peers:
            try: self.sock.sendto(data, (peer, self.port))
            except: pass
        print(f"[📡] Mesh: {type} {target} anunciado al enjambre.")

    def listen_for_peers(self):
        self.sock.bind(('0.0.0.0', self.port))
        while True:
            try:
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
                    print(f"[💉] Mesh: Inmunidad para {msg['target_type']} {target} sincronizada.")
            except: pass

    def check_reputation(self, ip, ja3=None):
        """Verifica IP y JA3 en la inteligencia compartida"""
        if ip in self.shared_intel["blacklist_ips"]:
            return True, "IP_BLACK"
        if ja3 and ja3 in self.shared_intel["blacklist_ja3"]:
            return True, "JA3_BLACK"
        return False, None

def start_mesh_service(node_id, peers):
    node = HellMeshNode(node_id, peers=peers)
    threading.Thread(target=node.listen_for_peers, daemon=True).start()
    return node
