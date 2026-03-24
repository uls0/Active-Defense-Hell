import os
import socket
import json
import time

HOST = ""os.getenv('PRO_IP')""
PORTS = [21, 22, 23, 25, 53, 80, 81, 88, 110, 111, 135, 137, 139, 143, 161, 179, 389, 443, 445, 502, 1433, 3306, 3389, 6443, 8080, 2375, 2376, 9100, 9090, 9200, 5601, 6379, 11211, 8081, 3000, 5000, 8000, 11434, 6666, 8888]

def scan_ports():
    results = {"OPEN": [], "CLOSED": [], "TIMEOUT": []}
    print(f"--- ESCANEANDO {HOST} ---")
    for port in PORTS:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        try:
            r = s.connect_ex((HOST, port))
            if r == 0:
                results["OPEN"].append(port)
                print(f"[+] {port} OPEN")
            else:
                results["CLOSED"].append(port)
        except:
            results["TIMEOUT"].append(port)
        finally:
            s.close()
    return results

if __name__ == "__main__":
    report = scan_ports()
    print(f"\nTOTAL ABIERTOS: {len(report['OPEN'])}")
    print(f"PUERTOS: {report['OPEN']}")
