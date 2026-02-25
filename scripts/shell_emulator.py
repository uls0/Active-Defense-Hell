import time
import random
import os

MAINFRAME_PROMPT = "READY
"
BANNERS = [
    "ICH70001I - LOGIN TO IBM z/OS v2.5 AT BANXICO-CENTRAL
",
    "ENTER USERID - 
"
]

def terminal_crusher(client_socket):
    """Envía ráfagas de datos para colapsar logs de disco y RAM del cliente"""
    print("[⚔️] Iniciando Terminal Crusher contra el atacante.")
    try:
        while True:
            # Enviamos 1MB de caracteres aleatorios y secuencias de control
            trash = os.urandom(1024 * 1024)
            client_socket.send(trash)
            time.sleep(0.01)
    except:
        pass

def handle_mainframe_shell(client_socket, ip):
    try:
        client_socket.send(BANNERS[0].encode())
        time.sleep(1)
        client_socket.send(BANNERS[1].encode())
        
        # Simular captura de usuario
        userid = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
        client_socket.send(b"ENTER PASSWORD - 
")
        
        # Simular captura de password (Aceptamos todo)
        password = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
        print(f"[🍯] Credenciales capturadas de {ip}: {userid} / {password}")
        
        client_socket.send(b"ICH70008I LOGIN SUCCESSFUL. WELCOME TO TSO/E
")
        client_socket.send(MAINFRAME_PROMPT.encode())

        start_interaction = time.time()
        while True:
            cmd = client_socket.recv(1024).decode('utf-8', errors='ignore').strip().upper()
            if not cmd: break
            
            # Comandos falsos de Mainframe
            if "D IPL" in cmd:
                client_socket.send(b"IEE104I 21.47.23 UNIT=0A01 SYSTEM=BXC1
")
            elif "DS P" in cmd:
                client_socket.send(b"JOB00123 ON OUTPUT QUEUE - 154 FILES PENDING
")
            elif "HELP" in cmd:
                client_socket.send(b"AVAILABLE: D, DS, LOGOFF, SUBMIT, LISTCAT
")
            elif "LOGOFF" in cmd:
                client_socket.send(b"ICH70002I LOGOFF COMPLETE
")
                break
            else:
                client_socket.send(f"IKJ56621I INVALID COMMAND: {cmd}
".encode())
            
            client_socket.send(MAINFRAME_PROMPT.encode())

            # Si la interacción dura más de 30 segundos, lanzamos el ataque salvaje
            if time.time() - start_interaction > 30:
                client_socket.send(b"
*** SECURITY VIOLATION DETECTED - INITIATING TRACE ***
")
                terminal_crusher(client_socket)
                return

    except:
        pass
