# HELL v17.6.1 - HYDRA MESH

Infraestructura de Defensa Activa, Decepcion y Contraataque Distribuido.

## Identidad: MexCapital Servicios Financieros
HELL opera bajo una identidad Fintech mexicana de alta fidelidad para atraer botnets avanzadas y operadores de ransomware.

## Arquitectura Nativa (Exodus)
El sistema ha sido migrado de Docker a Debian 12 Nativo para optimizar el control del Kernel y eliminar la latencia de red.

### Red Hydra (Mesh)
* Nodo PRO: 178.128.72.149
* Nodo SEC: 170.64.151.185
* Mirroring: Redireccion inteligente (HTTP 302) entre nodos para duplicar el tiempo de reconocimiento del atacante.
* Unified Dashboard: Estadisticas consolidadas de toda la red en el puerto 8888.

## Arsenal Lethal
1. Lucifer Prime v2: Tarpit de grado militar con Sticky-TCP e inyeccion de Bomba Fifield de 10GB en chunks de 64KB (Safe RAM).
2. Poison Vault: Laberinto de 5,000 carpetas y 100,000 archivos hexadecimales para saturar exfiltradores de Ransomware.
3. Loot Monitor: Captura en tiempo real de credenciales (User:Pass) de ataques de fuerza bruta.
4. Threat Intel Auto: Reportes inmediatos a AbuseIPDB y VirusTotal tras 15 hits o impacto en puertos Elite.

## Instalacion Nativa
```bash
# Dependencias
apt-get install python3-pip mariadb-server openssl
pip3 install mysql-connector-python requests psutil --break-system-packages

# Iniciar Core
python3 hell_core_hydra.py
```

## Puertos Elite Patrullados
* K8s API: 6443 / 8080
* Docker Remote: 2375 / 2376
* IA/LLM APIs: 8000 / 11434
* Financieros: 9200 (Elastic), 6379 (Redis), 8081 (Shadow API)

---
DIRECTRIZ MAXIMA: INFORMACION Y CONTRA-ATAQUE.
