FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para psutil y otras herramientas
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos del proyecto
COPY . .

# Instalar librerías de Python necesarias para HELL v8.9.1
RUN pip install --no-cache-dir \
    requests \
    psutil \
    flask \
    google-genai

# Exponer puertos (informativo, ya que usamos network_mode: host)
EXPOSE 80 443 445 3306 8888 2222

CMD ["python", "hell_core.py"]
