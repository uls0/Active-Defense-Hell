import socket
import threading
import json
import time
import os

class HellMeshNode:
    def __init__(self, node_id, port=9999, peers=None):
        self.node_id = node_id
        self.port = port
        self.peers = peers or [] # Lista de IPs de tus otros servidores HELL
        self.intel_file = "logs/mesh_intel.json"
        self.shared_intel = self.load_intel()
        
        # Socket UDP para comunicación ligera entre nodos
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def load_intel(self):
        """Carga la inteligencia compartida desde el disco"""
        if os.path.exists(self.intel_file):
            with open(self.intel_file, 'r') as f:
                return json.load(f)
        return {"blacklist": {}, "honey_tokens": []}

    def save_intel(self):
        """Guarda la inteligencia compartida"""
        with open(self.intel_file, 'w') as f:
            json.dump(self.shared_intel, f, indent=4)

    def broadcast_threat(self, ip, threat_level, details):
        """Anuncia una amenaza detectada a todos los nodos del Mesh"""
        message = {
            "node_origin": self.node_id,
            "type": "THREAT_ALERT",
            "target_ip": ip,
            "level": threat_level,
            "details": details,
            "timestamp": time.time()
        }
        data = json.dumps(message).encode()
        for peer in self.peers:
            try:
                self.sock.sendto(data, (peer, self.port))
            except:
                pass
        print(f"[📡] Mesh: Amenaza {ip} anunciada a {len(self.peers)} nodos.")

    def listen_for_peers(self):
        """Escucha anuncios de otros nodos del Mesh"""
        self.sock.bind(('0.0.0.0', self.port))
        print(f"[🌐] Nodo Mesh escuchando en puerto {self.port}...")
        
        while True:
            try:
                data, addr = self.sock.recvfrom(4096)
                msg = json.loads(data.decode())
                
                if msg["type"] == "THREAT_ALERT":
                    target_ip = msg["target_ip"]
                    # Agregamos a la lista negra local con fecha de expiración (24h)
                    self.shared_intel["blacklist"][target_ip] = {
                        "level": msg["level"],
                        "origin": msg["node_origin"],
                        "expires": msg["timestamp"] + 86400
                    }
                    self.save_intel()
                    print(f"[💉] Mesh: Inmunidad compartida recibida. IP {target_ip} bloqueada preventivamente.")
            except:
                pass

    def check_reputation(self, ip):
        """Verifica si una IP ya es conocida por el Mesh"""
        if ip in self.shared_intel["blacklist"]:
            return True, self.shared_intel["blacklist"][ip]
        return False, None

def start_mesh_service(node_id, peers):
    node = HellMeshNode(node_id, peers=peers)
    threading.Thread(target=node.listen_for_peers, daemon=True).start()
    return node
