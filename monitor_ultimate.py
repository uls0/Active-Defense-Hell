import os
import time
import re
import sys

LOG_FILE = "logs/hell_activity.log"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_stats():
    if not os.path.exists(LOG_FILE):
        return 0, 0, 0
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        total_data = sum(float(d) for d in re.findall(r"Injected: ([\d.]+)MB", content))
        total_time = sum(float(t) for t in re.findall(r"Time Lost: ([\d.]+)s", content))
        total_hits = len(re.findall(r"TRIGGERED:", content))
    return total_data, total_time, total_hits

def tail_f():
    print("\033[91m" + "💀 HELL ULTIMATE MONITOR - LIVE THREAT INTELLIGENCE" + "\033[0m")
    print("-" * 60)
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        f.seek(0, 2) # Ir al final del archivo
        while True:
            line = f.readline()
            if not line:
                # Mostrar resumen cada 5 segundos si no hay actividad
                data, secs, hits = get_stats()
                sys.stdout.write(f"[STATUS] Secured: {round(secs/3600, 2)}h | Data: {round(data/1024, 2)}GB | Hits: {hits}   ")
                sys.stdout.flush()
                time.sleep(1)
                continue
            
            # Formatear la salida para que sea legible
            if "TRIGGERED" in line:
                print("
\033[93m" + "!" * 60 + "\033[0m")
                print(f"\033[91m{line.strip()}\033[0m")
            elif "IP:" in line:
                print(f"\033[97m{line.strip()}\033[0m")
            elif "Actor:" in line:
                print(f"\033[92m{line.strip()}\033[0m")
            elif "THREAT NEUTRALIZED" in line:
                print(f"\033[94m{line.strip()}\033[0m")
            elif "TOTAL DAMAGE" in line:
                print(f"\033[92m{line.strip()}\033[0m")
                print("\033[93m" + "!" * 60 + "\033[0m")

if __name__ == "__main__":
    try:
        tail_f()
    except KeyboardInterrupt:
        print("

[i] Monitor finalizado. La guardia eterna continúa.")
