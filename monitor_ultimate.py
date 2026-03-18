import os
import time
import re
import sys
from datetime import datetime

LOG_FILE = "logs/hell_activity.log"

def get_stats():
    if not os.path.exists(LOG_FILE): return 0, 0, 0
    try:
        with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            data_matches = re.findall(r"Data: ([\d.]+)MB", content)
            time_matches = re.findall(r"Time Lost: ([\d.]+)s", content)
            total_data = sum(float(d) for d in data_matches)
            total_time = sum(float(t) for t in time_matches)
            total_hits = len(re.findall(r"TRIGGERED:", content)) + len(re.findall(r"HELL-LUCIFER", content))
            return total_data, total_time, total_hits
    except: return 0, 0, 0

def monitor_ultimate():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;91m" + "="*65 + "\033[0m")
    print("\033[1;91m" + "      💀 HELL MONITOR ULTIMATE v5.0 - LUCIFER RISING 💀" + "\033[0m")
    print("\033[1;97m" + f"             Sincronizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + "\033[0m")
    print("\033[1;91m" + "="*65 + "\033[0m")
    print("\033[90m" + "Protocolos: TITAN, HYDRA, CISCO-KILLER, HELL-LUCIFER (The Void)" + "\033[0m")
    print("-" * 65)
    
    if not os.path.exists(LOG_FILE):
        print("\033[93m[!] Esperando actividad en el log...\033[0m")

    with open(LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        f.seek(0, 2)
        
        while True:
            line = f.readline()
            if not line:
                data, secs, hits = get_stats()
                data_gb = data / 1024
                status_line = f"\r\033[1;97m[STATUS]\033[0m Secured: \033[1;92m{round(secs/3600, 2)}h\033[0m | Data: \033[1;91m{round(data*8, 2)} Mb\033[0m ({round(data_gb, 2)} GB) | Hits: \033[1;93m{hits}\033[0m   "
                sys.stdout.write(status_line)
                sys.stdout.flush()
                time.sleep(1)
                continue
            
            line_clean = line.strip()
            
            if "HELL-LUCIFER" in line_clean:
                print("\n\033[1;45;97m" + "🔱" * 28 + " LUCIFER " + "🔱" * 28 + "\033[0m")
                print(f"\033[1;95m{line_clean}\033[0m")
            
            elif "TRIGGERED" in line_clean:
                print("\n\033[1;91m" + "!" * 65 + "\033[0m")
                print(f"\033[1;91m{line_clean}\033[0m")
            
            elif "NEUTRALIZED" in line_clean:
                print(f"\033[1;94m{line_clean}\033[0m")
                print("\033[90m" + "-" * 65 + "\033[0m")
            
            elif "Target Port:" in line_clean:
                color = "\033[1;95m" if "(VOID RANGE)" in line_clean else "\033[1;97m"
                print(f"{color}{line_clean}\033[0m")

            elif "IP:" in line_clean or "Origin:" in line_clean:
                print(f"\033[1;97m{line_clean}\033[0m")
            
            elif "Action:" in line_clean or "Mode:" in line_clean:
                print(f"\033[1;93m    └─ {line_clean}\033[0m")

            else:
                if line_clean: print(line_clean)

if __name__ == "__main__":
    try:
        monitor_ultimate()
    except KeyboardInterrupt:
        print("\n\n\033[1;91m[!] Monitor Offline. El vacío persiste.\033[0m")
