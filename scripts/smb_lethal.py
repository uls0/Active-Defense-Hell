import os
import time
import random
import binascii

from scripts import zip_generator

def smb_infinite_maze(client_socket, tracker):
    """Laberinto infinito que entrega una Stealth Bolt de 1 Mb por cada señuelo."""
    header = binascii.unhexlify("fe534d4240000000000000000000000000000000000000000000000000000000")
    try:
        # Generar el payload una vez para eficiencia
        bolt_payload = zip_generator.generate_stealth_bolt()
        
        while True:
            fake_files = [b"NOMINA_EJECUTIVA.zip", b"ACCESOS_AWS.key.zip", b"BACKUP_DB_PROD.sql.zip", b"PASSWORDS_MONEX.txt.zip"]
            
            # Simulamos el envío del 'archivo'
            # Enviamos el header de SMB seguido de la Stealth Bolt de 1 Mb
            payload = header + random.choice(fake_files) + b" :: " + bolt_payload
            client_socket.send(payload)
            
            tracker['bytes'] += len(payload)
            print(f"[💀] SMB STEALTH BOLT (1 Mb) DEPLOYED via {random.choice(fake_files).decode()}")
            
            # Pausa para simular latencia de red real y maximizar retención
            time.sleep(random.uniform(2, 5))
    except: pass

def handle_smb_session(client_socket, ip):
    tracker = {'bytes': 0}
    # Siempre usamos el laberinto infinito para maximizar retención
    print(f"[🛡️] AD-FAKE: Iniciando Labyrinth con Infiltración de Archivos contra {ip}")
    smb_infinite_maze(client_socket, tracker)
    return tracker['bytes']
