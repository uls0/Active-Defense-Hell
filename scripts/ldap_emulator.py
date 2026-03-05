import time
import random
import socket

def handle_ldap_session(client_socket, ip):
    """
    Simula un Active Directory (LDAP) extremadamente lento y con objetos infinitos.
    """
    session_bytes = 0
    start_time = time.time()
    
    # Estructura de AD falsa
    BASE_DN = "DC=corp,DC=internal"
    OUS = ["Domain Admins", "Executive", "Finance", "HR", "IT_Infrastructure", "R&D_Project_X"]

    try:
        # 1. LDAP BIND (Simular autenticación exitosa)
        # Recibimos el paquete de Bind y respondemos OK tras un stall
        time.sleep(3.5)
        # Respuesta LDAP exitosa mínima (BindResponse)
        client_socket.send(b"\x30\x0c\x02\x01\x01\x61\x07\x0a\x01\x00\x04\x00\x04\x00")
        session_bytes += 14

        # 2. LDAP SEARCH (Entregar usuarios por goteo infinito)
        while True:
            elapsed = time.time() - start_time
            if elapsed > 7200: break # Limite de 2 horas por sesión
            
            ou = random.choice(OUS)
            user_id = random.randint(1000, 9999)
            user_dn = f"CN=user_{user_id},OU={ou},{BASE_DN}"
            
            # Simular un resultado de búsqueda de LDAP (SearchResultEntry)
            # Entregamos un objeto cada 3 segundos
            time.sleep(3.0)
            
            fake_entry = f"LDAP_OBJECT: {user_dn} | Attributes: [pwdLastSet=2026, userAccountControl=512, mail=user_{user_id}@corp.internal]\n"
            try:
                client_socket.send(fake_entry.encode())
                session_bytes += len(fake_entry)
                
                # Inyectar un latido TCP para evitar cierre
                client_socket.send(b"\x00") 
            except:
                break

    except Exception:
        pass
        
    return session_bytes
