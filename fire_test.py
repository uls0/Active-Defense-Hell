import socket
import time

def test_port(port, name, data=b"GET / HTTP/1.1\r\n\r\n"):
    print(f"[*] Testing {name} on port {port}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect(('127.0.0.1', port))
        
        if port == 22:
            time.sleep(0.5); s.send(b"root\n")
            time.sleep(0.5); s.send(b"root\n")
            time.sleep(0.5); s.send(b"whoami\n")
        elif port == 179:
            # BGP Open Marker
            s.send(b"\xff" * 16)
        else:
            s.send(data)
            
        response = s.recv(1024)
        if len(response) > 0:
            print(f"  [✅] Response received ({len(response)} bytes).")
        s.close()
    except Exception as e:
        print(f"  [❌] Port {port} error: {e}")

if __name__ == "__main__":
    print("=== HELL v9.0.9 FIRE TEST: TOTAL ARSENAL VALIDATION ===")
    test_port(22, "SSH Bait & Bomb")
    test_port(445, "AD SMB Labyrinth", data=b"\x00\x00\x00\x2f\xffSMB")
    test_port(3306, "MySQL Data Stream")
    test_port(179, "BGP Hijack Simulation")
    test_port(502, "SCADA CFE Simulator")
    test_port(8888, "Tactical Dashboard")
    print("=======================================================")
