import socket, time

def handle_mirage(client_socket, ip):
    """Protocolo RDP nativo simplificado (Mirage Mode)"""
    try:
        # X.224 Connection Request
        client_socket.recv(1024)
        # Connection Confirm (CC)
        client_socket.send(b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x12\x34\x00\x02\x01\x08\x00\x03\x00\x00\x00")
        time.sleep(0.5)
        # GCC Conference Create Response
        client_socket.send(b"\x03\x00\x00\x6b\x02\xf0\x80\x7f\x66\x82\x00\x62\x0a\x01\x00\x02\x01\x00\x30\x5a\x02\x01\x21\x04\x01\x01\x04\x01\x01\x01\x01\xff")
        # Inmortalizamos la sesion
        time.sleep(15)
    except: pass
    finally: client_socket.close()
