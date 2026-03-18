FROM python:3.10-slim

WORKDIR /app

# Actualización de sistema y herramientas de red necesarias para HELL
RUN apt-get update && apt-get install -y \
    iptables \
    netstat-nat \
    iproute2 \
    procps \
    curl \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Instalación de dependencias críticas (incluyendo Flask para el Dashboard)
RUN pip install --no-cache-dir \
    psutil \
    requests \
    cryptography \
    flask \
    flask-cors \
    python-dotenv \
    --break-system-packages

ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1

COPY . .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "hell_core.py"]
