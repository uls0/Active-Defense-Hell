import socket
import threading
import time
import paramiko

HOST = "170.64.151.185"
PORT = 6666

def monitor_server_resources():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(HOST, 22, "root", "INK0uJ8j4a5xCR", timeout=10)
        print("[🔎] Monitoreo iniciado...")
        cmd = "ps -o rss,command -p $(pgrep -f lucifer_prime.py) | tail -n 1 && tail -n 2 /root/Active-Defense-Hell/logs/lucifer_prime.log"
        for _ in range(4):
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(f"--- SERVER STATS ---\n{stdout.read().decode().strip()}")
            time.sleep(3)
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

def simulate_bot_attack():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((HOST, PORT))
        print(f"[🔥] Bot Conectado. Enviando TRIGGER...")
        s.sendall(b"GET /financial_data_backup HTTP/1.1\r\n\r\n")
        total_received = 0
        for _ in range(50):
            data = s.recv(65536)
            if not data: break
            total_received += len(data)
        print(f"[✔] Bot recibió {total_received / 1024 / 1024:.2f} MB de datos tóxicos.")
        s.close()
    except Exception as e:
        print(f"Error bot: {e}")

if __name__ == "__main__":
    t_mon = threading.Thread(target=monitor_server_resources)
    t_bot = threading.Thread(target=simulate_bot_attack)
    t_mon.start()
    time.sleep(2)
    t_bot.start()
    t_mon.join()
    t_bot.join()
