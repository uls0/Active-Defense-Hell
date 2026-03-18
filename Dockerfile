FROM python:3.10-slim

WORKDIR /app

# Usar mirrors alternativos si el principal falla
RUN sed -i 's/deb.debian.org/ftp.us.debian.org/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    iptables \
    netstat-nat \
    iproute2 \
    procps \
    curl \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias rompiendo el bloqueo de paquetes del sistema (modo contenedor)
RUN pip install --no-cache-dir psutil requests cryptography --break-system-packages

ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1

COPY . .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "hell_core.py"]
