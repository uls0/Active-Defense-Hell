FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir \
    requests \
    psutil \
    flask \
    google-genai

# -u activa el modo unbuffered (vital para ver logs en Docker)
CMD ["python", "-u", "hell_core.py"]
