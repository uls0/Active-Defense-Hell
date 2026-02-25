import socket
import time

def test_port(port, name, data=b"GET / HTTP/1.1

"):
    print(f"[*] Testing {name} on port {port}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(('127.0.0.1', port))
        s.send(data)
        response = s.recv(1024)
        print(f"  [✅] Response received from {name}. System is ACTIVE.")
        s.close()
    except Exception as e:
        print(f"  [❌] Port {port} ({name}) is NOT responding: {e}")

if __name__ == "__main__":
    print("=== HELL FIRE TEST: OPERATIONAL VERIFICATION ===")
    test_port(80, "Web/OWA Trap")
    test_port(445, "Active Directory Trap", data=b"\x00\x00\x00\x2f\xffSMB")
    test_port(22, "Bait & Switch SSH")
    test_port(3306, "MySQL Data Bomb")
    test_port(8888, "Tactical Dashboard")
    print("=================================================")
