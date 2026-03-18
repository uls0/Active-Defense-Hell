import socket

def start_void(log_callback):
    host = '0.0.0.0'
    port = 6666
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((host, port))
        server.listen(1000)
        while True:
            client, addr = server.accept()
            log_callback(addr[0], port, "TRAPPED IN THE ABYSS")
            client.close()
    except: pass
