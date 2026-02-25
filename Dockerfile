FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias esenciales de red y compilación
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    iproute2 \
    iptables \
    net-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Instalar librerías de Python para v10.6.2
RUN pip install --no-cache-dir \
    requests \
    psutil \
    flask \
    google-genai

RUN chmod +x entrypoint.sh check_hell.sh

# Exponer el arsenal de puertos
EXPOSE 22 80 443 445 179 502 3306 8888

ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3", "-u", "hell_core.py"]
