# 💀 Proyecto HELL: Sistema de Defensa Activa con IA

**HELL (Honeypot Exploitation & Lethal Logging)** es un sistema de defensa activa diseñado para detectar, ralentizar y neutralizar atacantes mediante técnicas de "tarpit", contraataques de saturación y análisis de comportamiento mediante IA.

---

## 🚀 Características Principales

- **🧠 IA Adaptive Defense:** Integración con Google Gemini (1.5 Flash) para distinguir entre bots genéricos, humanos y agentes de pentesting autónomos de Hugging Face.
- **🧨 Contraataques Activos:**
  - **Gzip Bomb:** Entrega de un archivo de 10GB comprimido en pocos MB para colapsar la RAM del atacante.
  - **Infinite Stream:** Flujo de datos basura a 5MB/s para saturar su ancho de banda.
- **🕸️ Tarpits Multicapa:**
  - **SMTP (Puerto 25):** Ralentización extrema de conexiones de correo.
  - **MySQL (Puerto 3306):** Bucle infinito de autenticación falsa para bots de bases de datos.
- **📡 Threat Intel:** Reporte automático de IPs atacantes a **VirusTotal** mediante la API de comunidad.
- **📊 Monitor en Vivo:** Panel en terminal para seguimiento de ataques en tiempo real.

---

## 🛠️ Requisitos

- **Docker & Docker Compose**
- **Python 3.9+** (Para ejecución local)
- **API Keys** (Opcional pero recomendado):
  - [Google AI Studio (Gemini)](https://aistudio.google.com/)
  - [VirusTotal API](https://www.virustotal.com/)

---

## 📦 Instalación y Despliegue

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/uls0/Active-Defense-Hell.git
   cd Active-Defense-Hell
   ```

2. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Edita el archivo .env con tus llaves
   ```

3. **Levantar con Docker:**
   ```bash
   docker-compose up -d --build
   ```

4. **Monitorear actividad:**
   ```bash
   python monitor_hell.py
   ```

---

## ⚠️ Advertencia Legal
Este software es una herramienta de seguridad defensiva. El uso de contraataques activos debe realizarse bajo entornos controlados y cumpliendo con las normativas locales de ciberseguridad. El autor no se hace responsable del mal uso de esta herramienta.

---

**Desarrollado por Ulises Guzmán & Gemini CLI**
*"Si entras en el infierno, asegúrate de no poder salir."*
