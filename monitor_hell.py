import os
import time
from datetime import datetime

LOG_FILE = "logs/hell_activity.log"

def monitor_hell():
    print("="*50)
    print("      💀 PROYECTO HELL: PANEL DE MONITOREO 💀")
    print("="*50)
    print(f"Iniciando seguimiento en: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*50)
    
    # Crear log si no existe
    if not os.path.exists(LOG_FILE):
        os.makedirs("logs", exist_ok=True)
        with open(LOG_FILE, "w") as f:
            f.write(f"[{datetime.now()}] Sistema de Monitoreo Iniciado.
")

    try:
        with open(LOG_FILE, "r") as f:
            # Ir al final del archivo
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(1)
                    continue
                
                # Resaltar ataques detectados
                if "[🔥]" in line:
                    print(f"\033[91m{line.strip()}\033[0m") # Rojo para Gzip Bomb
                elif "[🤖]" in line:
                    print(f"\033[94m{line.strip()}\033[0m") # Azul para IA
                elif "[🌊]" in line:
                    print(f"\033[93m{line.strip()}\033[0m") # Amarillo para Infinite Stream
                else:
                    print(line.strip())
                    
    except KeyboardInterrupt:
        print("
[i] Cerrando monitor...")

if __name__ == "__main__":
    monitor_hell()
