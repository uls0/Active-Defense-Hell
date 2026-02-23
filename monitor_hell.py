import os
import time
from datetime import datetime

LOG_FILE = "logs/hell_activity.log"

def monitor_hell():
    print("="*60)
    print("      💀 PROYECTO HELL: PANEL DE MONITOREO REAL-TIME 💀")
    print("="*60)
    print(f"Sesión iniciada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*60)
    
    # Asegurar que la carpeta y el log existen
    if not os.path.exists("logs"):
        os.makedirs("logs", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write(f"[{datetime.now()}] Sistema de Monitoreo Iniciado.\n")

    try:
        with open(LOG_FILE, "r") as f:
            # Ir al final del archivo para ver solo lo nuevo
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(1)
                    continue
                
                # Colores ANSI para terminal Linux
                line = line.strip()
                if "[🔥]" in line:
                    print(f"\033[91m{line}\033[0m") # Rojo (Gzip Bomb)
                elif "[🤖]" in line:
                    print(f"\033[94m{line}\033[0m") # Azul (IA Analysis)
                elif "[🌊]" in line:
                    print(f"\033[93m{line}\033[0m") # Amarillo (Entropy Flood)
                elif "[👑]" in line:
                    print(f"\033[92m{line}\033[0m") # Verde (Whitelist Bypass)
                elif "[🕵️]" in line:
                    print(f"\033[95m{line}\033[0m") # Magenta (Cerberus Token)
                else:
                    print(line)
                    
    except KeyboardInterrupt:
        print("\n[i] Monitor finalizado.")

if __name__ == "__main__":
    monitor_hell()
