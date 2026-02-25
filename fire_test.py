import socket
import time

def test_port(port, name, data=b"GET / HTTP/1.1\r\n\r\n"):
    print(f"[*] Testing {name} on port {port}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect(('127.0.0.1', port))
        
        # Para el puerto 22, simulamos un login rápido para ver si escupe la bomba
        if port == 22:
            time.sleep(1)
            s.send(b"root\n")
            time.sleep(1)
            s.send(b"root\n")
            time.sleep(1)
            s.send(b"ls\n")
        else:
            s.send(data)
            
        response = s.recv(4096)
        if len(response) > 0:
            print(f"  [✅] Response received ({len(response)} bytes). System is ACTIVE.")
            if port == 22 and len(response) > 1000:
                print("  [💀] SSH BOMB DETECTED IN RESPONSE! EXPLOIT IS READY.")
        s.close()
    except Exception as e:
        print(f"  [❌] Port {port} ({name}) error: {e}")

if __name__ == "__main__":
    print("=== HELL v9.0.3 FIRE TEST: PURE STABLE EDITION ===")
    test_port(22, "SSH Bait & Bomb")
    test_port(445, "Active Directory Trap", data=b"\x00\x00\x00\x2f\xffSMB")
    test_port(3306, "MySQL Data Bomb")
    test_port(8888, "Tactical Dashboard")
    print("==================================================")
