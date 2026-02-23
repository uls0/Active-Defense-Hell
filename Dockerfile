FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir google-generativeai requests

# Exponer el puerto del Tarpit
EXPOSE 8080

# Comando para ejecutar el core
CMD ["python", "hell_core.py"]
