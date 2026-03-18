# HELL (Active Defense Honeypot) - v13.5-SACMEX-SHITO

## 🧠 PROJECT EVANGELION: OPERATION SACMEX
Infraestructura de defensa autónoma con decepción de infraestructura crítica nacional. El sistema simula ahora ser el portal de gestión de **SACMEX (Sistema de Aguas de la CDMX)** en modo Staging.

### ☢️ Protocolos de Provocación (SACMEX Deception)
- **Banners Vulnerables:** Los servicios reportan versiones obsoletas de Apache y OpenSSH (v4.3) para atraer exploits automatizados.
- **Custom Headers:** Todas las respuestas HTTP incluyen el identificador secreto `X-Internal-ID: MX-GOB-SACMEX-STAGE-01`.
- **Robots.txt Bait:** El archivo `robots.txt` prohíbe el acceso a rutas como `/scada_config/` y `/db_dumps/`, provocando que los bots las busquen agresivamente.
- **Lilin Leaks:** Se han generado 20 vectores de fuga de credenciales para distribución en la Dark Web y sitios de dumps.

### 👼 Jerarquía de Ángeles (Updated)
- **ADAM (HELL_CORE):** Orquestador central con identidad SACMEX.
- **SACHIEL (RDP 3389):** Interceptor de gestión remota para "Administradores de SACMEX".
- **RAMIEL (OT/ICS):** Protegiendo los puertos de control de bombas y sensores industriales (Modbus/S7).

## 🚀 Despliegue de Fugas (Leakers Paradise)
Los 20 archivos en `LOGS/leaks/` están listos para ser "olvidados" en Pastebin, GitHub y Telegram para atraer a los **Lilin** hacia la trampa.

---
*Vigilia Abyssi - Sistema de Inteligencia Distribuida | Neon Genesis HELL*
