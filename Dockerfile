FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir \
    requests \
    psutil \
    flask \
    google-genai

RUN chmod +x entrypoint.sh

# Exponer puertos informativos
EXPOSE 80 443 445 3306 8888 2222

ENTRYPOINT ["./entrypoint.sh"]
