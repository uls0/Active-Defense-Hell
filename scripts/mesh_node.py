import socket
import threading
import json
import time
import os
import psutil # Requiere instalación: pip install psutil

class HellMeshNode:
    def __init__(self, node_id, port=9999, peers=None):
        self.node_id = node_id
        self.port = port
        self.peers = peers or []
        self.intel_file = "logs/mesh_intel.json"
        self.shared_intel = self.load_intel()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.load_avg = 0 # 0 a 100% de ocupación de hilos
        
    def load_intel(self):
        if os.path.exists(self.intel_file):
            with open(self.intel_file, 'r') as f:
                return json.load(f)
        return {"blacklist_ips": {}, "blacklist_ja3": {}, "peers_load": {}}

    def save_intel(self):
        with open(self.intel_file, 'w') as f:
            json.dump(self.shared_intel, f, indent=4)

    def broadcast_load(self, current_threads, max_threads):
        """Anuncia la carga actual del nodo al Mesh"""
        self.load_avg = (current_threads / max_threads) * 100
        message = {
            "node_origin": self.node_id,
            "type": "LOAD_UPDATE",
            "load": self.load_avg,
            "timestamp": time.time()
        }
        data = json.dumps(message).encode()
        for peer in self.peers:
            try: self.sock.sendto(data, (peer, self.port))
            except: pass

    def listen_for_peers(self):
        self.sock.bind(('0.0.0.0', self.port))
        while True:
            try:
                data, addr = self.sock.recvfrom(4096)
                msg = json.loads(data.decode())
                
                if msg["type"] == "LOAD_UPDATE":
                    self.shared_intel["peers_load"][msg["node_origin"]] = {
                        "ip": addr[0],
                        "load": msg["load"],
                        "last_seen": msg["timestamp"]
                    }
                    self.save_intel()
                
                elif msg["type"] == "THREAT_ALERT":
                    # (Lógica de JA3/IP anterior se mantiene aquí)
                    pass
            except: pass

    def get_best_node(self):
        """Busca el nodo con menos carga para delegar ataques"""
        if not self.shared_intel["peers_load"]: return None
        
        # Filtramos nodos que no hayamos visto en más de 5 min
        valid_peers = {k: v for k, v in self.shared_intel["peers_load"].items() if time.time() - v["last_seen"] < 300}
        if not valid_peers: return None
        
        best_node = min(valid_peers, key=lambda k: valid_peers[k]["load"])
        return valid_peers[best_node]["ip"]
