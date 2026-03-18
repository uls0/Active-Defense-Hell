import time, random

def handle_drip(client_socket, ip, port):
    """Atrapa al bot en un bucle de latencia infinita"""
    try:
        client_socket.send(b"READY\n")
        while True:
            time.sleep(random.uniform(15, 30))
            client_socket.send(b"\x00")
    except: pass
    finally: client_socket.close()
