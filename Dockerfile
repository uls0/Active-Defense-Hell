FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos del proyecto
COPY . .

# Instalar el nuevo SDK google-genai y requests
RUN pip install --no-cache-dir google-genai requests

# Exponer el puerto del Tarpit
EXPOSE 8080

# Comando para ejecutar el core
CMD ["python", "hell_core.py"]
