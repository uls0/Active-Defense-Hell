import os
import time
import re
import sys
from datetime import datetime

LOG_FILE = "logs/hell_activity.log"

def get_stats():
    """Calcula estadísticas rápidas leyendo solo el final del log si es muy grande"""
    if not os.path.exists(LOG_FILE): return 0, 0, 0
    try:
        # Para eficiencia en logs gigantes, leemos los últimos 2MB para estadísticas recientes
        # O leemos completo si es manejable. Aquí usamos un enfoque híbrido.
        with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Extraer de las líneas de daño acumulado para mayor precisión
            data_matches = re.findall(r"Data: ([\d.]+)MB", content)
            time_matches = re.findall(r"Time Lost: ([\d.]+)s", content)
            total_data = sum(float(d) for d in data_matches)
            total_time = sum(float(t) for t in time_matches)
            total_hits = len(re.findall(r"TRIGGERED:", content)) + len(re.findall(r"AETERNUM-DETECTION", content))
            return total_data, total_time, total_hits
    except: return 0, 0, 0

def monitor_ultimate():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;91m" + "="*65 + "\033[0m")
    print("\033[1;91m" + "      💀 HELL MONITOR ULTIMATE v4.0 - DEEP DECEPTION 💀" + "\033[0m")
    print("\033[1;97m" + f"             Sincronizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + "\033[0m")
    print("\033[1;91m" + "="*65 + "\033[0m")
    print("\033[90m" + "Protocolos Activos: TITAN, HYDRA-GORGON, AETERNUM-SENTINEL" + "\033[0m")
    print("-" * 65)
    
    if not os.path.exists(LOG_FILE):
        print("\033[93m[!] Esperando actividad en el log...\033[0m")

    with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        # Ir al final del archivo
        f.seek(0, 2)
        
        while True:
            line = f.readline()
            if not line:
                # Actualizar barra de estado en la misma línea
                data, secs, hits = get_stats()
                # Convertir a GB si es mucho, si no Mb (Megabits)
                data_gb = data / 1024
                status_line = f"\r\033[1;97m[STATUS]\033[0m Secured: \033[1;92m{round(secs/3600, 2)}h\033[0m | Data: \033[1;91m{round(data*8, 2)} Mb\033[0m ({round(data_gb, 2)} GB) | Hits: \033[1;93m{hits}\033[0m   "
                sys.stdout.write(status_line)
                sys.stdout.flush()
                time.sleep(1)
                continue
            
            # --- Lógica de Colores y Formateo ---
            line_clean = line.strip()
            
            if "AETERNUM-DETECTION" in line_clean:
                print("\n\033[1;41;97m" + "☢️" * 31 + " AETERNUM " + "☢️" * 24 + "\033[0m")
                print(f"\033[1;91m{line_clean}\033[0m")
            
            elif "TRIGGERED" in line_clean:
                print("\n\033[1;91m" + "!" * 65 + "\033[0m")
                print(f"\033[1;91m{line_clean}\033[0m")
            
            elif "NEUTRALIZED" in line_clean:
                print(f"\033[1;94m{line_clean}\033[0m")
                print("\033[90m" + "-" * 65 + "\033[0m")
            
            elif "ATTACK TYPE" in line_clean:
                print(f"\033[1;93m    └─ {line_clean}\033[0m")
            
            elif "CLOSURE STATE" in line_clean:
                color = "\033[1;92m" if "CLEAN" in line_clean else "\033[1;91m"
                print(f"{color}    └─ {line_clean}\033[0m")
            
            elif "SESSION DATA" in line_clean or "SESSION TIME" in line_clean:
                print(f"\033[96m    └─ {line_clean}\033[0m")
            
            elif "IP:" in line_clean or "Origin:" in line_clean or "Network:" in line_clean:
                print(f"\033[1;97m{line_clean}\033[0m")
            
            elif "[🔥]" in line_clean or "TITAN" in line_clean:
                print(f"\033[91m{line_clean}\033[0m")
            
            elif "[🛡️]" in line_clean or "HYDRA" in line_clean:
                print(f"\033[96m{line_clean}\033[0m")
            
            elif "TOTAL DAMAGE" in line_clean:
                print(f"\033[1;95m    └─ {line_clean}\033[0m")
            
            else:
                if line_clean: print(line_clean)

if __name__ == "__main__":
    try:
        monitor_ultimate()
    except KeyboardInterrupt:
        print("\n\n\033[1;91m[!] Monitor Offline. Los bots siguen en el infierno.\033[0m")
