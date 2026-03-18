import socket
import time
import sys

def simulate_attack():
    target_ip = "178.128.72.149"
    
    print(f"[*] INICIANDO SECUENCIA LILIN CONTRA ADAM ({target_ip})...")
    
    # FASE 1: SCANNING (Puertos variados)
    print("[1] FASE: SCANNING (Pattern Yellow)")
    ports = [22, 80, 443, 8080, 8443, 23, 1433, 3306]
    for p in ports:
        try:
            s = socket.create_connection((target_ip, p), timeout=0.5)
            s.send(b"GET / HTTP/1.1\r\nHost: 178.128.72.149\r\n\r\n")
            s.close()
            print(f"  > Port {p}: Connection Attempted.")
            time.sleep(0.5)
        except: pass

    # FASE 2: ENGAGED (RDP Engagement)
    print("[2] FASE: ENGAGED (Pattern Orange) - Intercepted by SACHIEL")
    try:
        s = socket.create_connection((target_ip, 3389), timeout=5)
        print("  > RDP 3389: Connection Established. Handshaking...")
        s.send(b"\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00")
        time.sleep(2) 
        s.close()
    except Exception as e:
        print(f"  > RDP Failed: {e}")

    # FASE 3: NEUTRALIZED (OT/ICS Target)
    print("[3] FASE: NEUTRALIZED (Pattern Red) - Target RAMIEL")
    try:
        s = socket.create_connection((target_ip, 502), timeout=5)
        print("  > MODBUS 502: Sending Industrial Payload...")
        s.send(b"\x00\x01\x00\x00\x00\x06\x01\x03\x00\x00\x00\x0a")
        time.sleep(1)
        s.close()
    except Exception as e:
        print(f"  > OT Failed: {e}")

    print("[*] SECUENCIA LILIN COMPLETADA. REVISAR MAGI DASHBOARD.")

if __name__ == "__main__":
    simulate_attack()
