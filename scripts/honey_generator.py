import os
from scripts import canary_generator

def generate_decoy_set(ip):
    """Genera un set de archivos carnada para una IP específica"""
    decoy_dir = f"logs/forensics/decoys_{ip}"
    os.makedirs(decoy_dir, exist_ok=True)
    
    # 1. Documento de Nómina (Canary PDF)
    nomina_path = os.path.join(decoy_dir, "NOMINA_EJECUTIVA_2026.pdf")
    with open(nomina_path, "wb") as f:
        # Usamos el generador de canarios que ya tenemos
        f.write(canary_generator.generate_canary_pdf("MY_IP_HERE", f"SMB_NOMINA_{ip}"))
    
    # 2. Archivo de contraseñas (Texto plano falso)
    creds_path = os.path.join(decoy_dir, "ACCESOS_VPN_PROD.txt")
    with open(creds_path, "w") as f:
        f.write("SERVER: vpn.mac-mx.com
USER: uguzman
PASS: MasterTv.2026!
TOKEN: 882931
")
        
    return decoy_dir

def get_decoy_file(filename, ip):
    """Simula la entrega de un archivo carnada"""
    if "NOMINA" in filename.upper():
        return canary_generator.generate_canary_pdf("MY_IP_HERE", f"EXFIL_{ip}")
    return b"ACCESS DENIED: Resource encrypted by Sentinel-Shield."
