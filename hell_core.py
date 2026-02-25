import socket
import threading
import time
import os
import sys
import signal
from scripts import smb_lethal, shell_emulator, k8s_emulator, scada_emulator, zip_generator, icmp_tarpit, network_mangler, abuse_generator, ja3_engine, predictive_ai, database_emulator, forensics_engine, profiler_engine, self_healing

print("[*] BOOT: HELL CORE v9.1.4 Initializing...")

HOST = '0.0.0.0'
PORTS = [80, 443, 445, 2222, 3306, 1433, 3389, 389, 88, 502, 8080, 8443, 9200]
LOG_FILE = "logs/hell_activity.log"

class HellServer:
    def __init__(self):
        os.makedirs("logs/forensics", exist_ok=True)
        self.stats = {}
        self.ai = predictive_ai.HellPredictiveAI()
        self.profiler = profiler_engine.HellProfiler()
        threading.Thread(target=self_healing.health_monitor_loop, daemon=True).start()

    def handle_client(self, client_socket, addr, local_port):
        ip = addr[0]
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[🔥] CONNECTION FROM {ip} ON PORT {local_port}")
        
        try:
            client_socket.settimeout(10.0)
            if local_port in [445, 4455]:
                smb_lethal.handle_smb_session(client_socket, ip)
            elif local_port in [22, 2222]:
                shell_emulator.handle_cowrie_trap(client_socket, ip)
            elif local_port == 3306:
                database_emulator.handle_mysql_trap(client_socket)
            else:
                while True:
                    client_socket.send(b"\x00")
                    time.sleep(30)
        except: pass
        finally:
            try: client_socket.close()
            except: pass

    def start_listener(self, port):
        """Intento persistente de apertura de puerto"""
        while True:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                server.bind((HOST, port))
                server.listen(200)
                print(f"[✅] PORT {port}: ACTIVE")
                while True:
                    client, addr = server.accept()
                    threading.Thread(target=self.handle_client, args=(client, addr, port), daemon=True).start()
            except Exception as e:
                # Si el puerto está ocupado, esperamos 30 segundos y re-intentamos
                time.sleep(30)

    def start(self):
        for port in PORTS:
            threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
        print("[🚀] HELL CORE v9.1.4: READY FOR COMBAT.")
        while True:
            try: time.sleep(1)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    HellServer().start()
