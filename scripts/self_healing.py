import os
import shutil
import time
import json

def perform_cleanup():
    """Realiza limpieza de archivos viejos para proteger el disco"""
    now = time.time()
    retention_days = 7
    seconds_in_day = 86400
    
    dirs_to_clean = ["logs/forensics", "logs/malware", "logs/abuse_reports"]
    
    print("[🧹] Inmune-System: Iniciando purga de archivos antiguos...")
    
    for folder in dirs_to_clean:
        if not os.path.exists(folder): continue
        for f in os.listdir(folder):
            path = os.path.join(folder, f)
            # Eliminar si el archivo tiene más de X días
            if os.stat(path).st_mtime < (now - (retention_days * seconds_in_day)):
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"    └─ Eliminado: {f}")

def check_disk_space():
    """Verifica si queda espacio suficiente en el servidor"""
    total, used, free = shutil.disk_usage("/")
    percent_free = (free / total) * 100
    return percent_free

def health_monitor_loop():
    """Hilo persistente de mantenimiento"""
    while True:
        perform_cleanup()
        free_space = check_disk_space()
        
        if free_space < 10:
            print(f"[🚨] CRITICAL: Solo queda {round(free_space, 2)}% de disco. HELL entrando en modo ahorro.")
            # Aquí podríamos activar una bandera global
            
        time.sleep(3600) # Ejecutar cada hora

if __name__ == "__main__":
    perform_cleanup()
