import os
import time
import re
import sys

LOG_FILE = "logs/hell_activity.log"

def get_stats():
    if not os.path.exists(LOG_FILE): return 0, 0, 0
    try:
        with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Regex específica para evitar duplicados: solo cuenta el daño de neutralizaciones individuales
            total_data = sum(float(d) for d in re.findall(r"Current Retention: .*? \| Data: ([\d.]+)MB", content))
            total_time = sum(float(t) for t in re.findall(r"Current Retention: ([\d.]+)s", content))
            total_hits = len(re.findall(r"TRIGGERED:", content))
            return total_data, total_time, total_hits
    except: return 0, 0, 0

def tail_f():
    print("\033[1;91m" + "💀 HELL MONITOR v3.2 - PURE PRECISION" + "\033[0m")
    print("\033[90m" + "Designed by ULSO+GCLI | Stable Deception Tracking" + "\033[0m")
    print("-" * 65)
    
    if not os.path.exists(LOG_FILE): open(LOG_FILE, 'a').close()

    with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                data, secs, hits = get_stats()
                sys.stdout.write(f"\r[STATUS] Secured: {round(secs/3600, 2)}h | Data: {round(data/1024, 2)}GB | Hits: {hits}   ")
                sys.stdout.flush()
                time.sleep(1)
                continue
            
            if "TRIGGERED" in line:
                print("\n\033[1;91m" + "!" * 65 + "\033[0m")
                print(f"\033[1;91m{line.strip()}\033[0m")
            elif "NEUTRALIZED" in line:
                print(f"\033[1;94m{line.strip()}\033[0m")
            elif "TOTAL DAMAGE" in line:
                print(f"\033[1;92m{line.strip()}\033[0m")
                print("\033[90m" + "-" * 65 + "\033[0m")
            elif "IP:" in line or "Actor:" in line or "Origin:" in line:
                print(f"\033[97m{line.strip()}\033[0m")

if __name__ == "__main__":
    try:
        tail_f()
    except KeyboardInterrupt:
        print("\n\n[i] Monitor finalizado.")
