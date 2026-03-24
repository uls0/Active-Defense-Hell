import paramiko
import re
import os
from collections import Counter

# CONFIGURACION VPS (PROYECTO HELL)
HOST = '178.128.72.149'
PORT = 2200
USER = 'root'
PASS = 'INK0uJ8j4a5xCn'
LOG_PATH = '/root/Active-Defense-Hell/logs/hell_activity.log'
MINI_LOG_PATH = '/root/Active-Defense-Hell/logs/lucifer_mini.log'

def get_top_void_ports():
    """
    Se conecta al VPS y extrae los 500 puertos mas atacados en el rango del Void.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"[*] Conectando a {HOST}:{PORT}...")
        ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=30)
        
        # Comando para extraer puertos del log principal
        cmd_main = "grep 'Target Port:' " + LOG_PATH + " | grep '(VOID RANGE)'"
        print("[*] Analizando log principal...")
        
        stdin, stdout, stderr = ssh.exec_command(cmd_main)
        main_output = stdout.read().decode('utf-8', errors='ignore')
        
        # Regex para extraer el numero de puerto: "Target Port: 12345"
        found_ports = re.findall(r'Target Port: (\d+)', main_output)
        
        # Si el log principal esta vacio, intentamos con el mini log (Lucifer Void)
        if not found_ports:
            print("[!] Sin resultados en el log principal. Consultando mini-log...")
            cmd_mini = "cat " + MINI_LOG_PATH
            stdin, stdout, stderr = ssh.exec_command(cmd_mini)
            mini_output = stdout.read().decode('utf-8', errors='ignore')
            
            # Formato en mini-log: "PORT:12345"
            found_ports = re.findall(r'PORT:(\d+)', mini_output)
            
        # Filtrar por rango del Void (20101-65534)
        void_ports = []
        for p in found_ports:
            try:
                p_int = int(p)
                if 20101 <= p_int <= 65534:
                    void_ports.append(p_int)
            except ValueError:
                continue
        
        if not void_ports:
            print("[!] No se detectaron puertos en el rango del Void (20101-65534).")
            return

        # Contar y obtener top 500
        stats = Counter(void_ports).most_common(500)
        
        # Guardar resultados
        output_file = 'void_top_500_analysis.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("--- ANALISIS DE PUERTOS TOP VOID ---\n")
            for port, count in stats:
                f.write(f"Puerto: {port} | Hits: {count}\n")
        
        print(f"[OK] Analisis completado. {len(stats)} puertos registrados en {output_file}")
        
        # Mostrar Top 10 en consola
        print("\n--- RESUMEN TOP 10 ---")
        for port, count in stats[:10]:
            print(f"-> {port}: {count} hits")

    except Exception as e:
        print(f"[!] Error critico: {str(e)}")
    finally:
        ssh.close()

if __name__ == "__main__":
    get_top_void_ports()
