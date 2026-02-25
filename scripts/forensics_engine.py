import os
import zipfile
import time
import shutil

def create_evidence_pack(ip, session_id):
    """
    Compila un paquete ZIP con toda la evidencia recolectada de un atacante.
    """
    forensics_dir = "logs/forensics"
    os.makedirs(forensics_dir, exist_ok=True)
    
    timestamp = int(time.time())
    pack_name = f"{forensics_dir}/EVIDENCE_{ip}_{timestamp}.zip"
    
    with zipfile.ZipFile(pack_name, 'w') as zipf:
        # 1. Incluir Reporte de Abuso (si existe)
        abuse_dir = "logs/abuse_reports"
        for f in os.listdir(abuse_dir):
            if ip in f:
                zipf.write(os.path.join(abuse_dir, f), f"abuse_report/{f}")
        
        # 2. Incluir Malware Capturado (si existe)
        malware_dir = "logs/malware"
        for f in os.listdir(malware_dir):
            if ip in f:
                zipf.write(os.path.join(malware_dir, f), f"malware_samples/{f}")
        
        # 3. Incluir Logs del Sistema relacionados
        log_file = "logs/hell_activity.log"
        if os.path.exists(log_file):
            # Extraer solo las líneas de esta IP para no inflar el ZIP
            with open(log_file, "r", encoding='utf-8') as f:
                lines = [line for line in f.readlines() if ip in line]
                zipf.writestr("attack_history.log", "".join(lines))
        
        # 4. Metadatos de la sesión
        metadata = f"Evidence Pack for IP: {ip}
Session ID: {session_id}
Timestamp: {time.ctime()}
"
        zipf.writestr("metadata.txt", metadata)

    print(f"[📂] Forensic Pack creado para {ip}: {pack_name}")
    return pack_name
