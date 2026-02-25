FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    iproute2 \
    iptables \
    net-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir \
    requests \
    psutil \
    flask \
    google-genai

RUN chmod +x entrypoint.sh

EXPOSE 80 443 445 3306 8888 2222

# El comando por defecto ahora es el CORE
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3", "-u", "hell_core.py"]
