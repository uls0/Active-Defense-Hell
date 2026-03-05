import socket
import threading
import time
import json
import random
import os
import requests
from flask import request

# Configuración de Puertos
OLLAMA_PORT = 11434
KUBE_PORT = 6443
LOG_FILE = "logs/hell_activity.log"

def log_event(ip, port, msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    report = f"\n[🧠 NEURAL-KUBE-TRAP]: {timestamp}\n----------------------------------------\nIP: {ip} | Port: {port}\nAction: {msg}\n----------------------------------------\n"
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(report)

def handle_ollama(client_socket, addr):
    """Simula una API de Ollama (IA) desprotegida."""
    ip = addr[0]
    try:
        client_socket.settimeout(10)
        request_data = client_socket.recv(1024).decode('utf-8', errors='ignore')
        
        if "GET /api/tags" in request_data:
            log_event(ip, OLLAMA_PORT, "Querying AI Models (Bait Triggered)")
            models = {
                "models": [
                    {"name": "llama3:70b-corp-confidential", "size": "40GB", "modified_at": "2026-02-27T10:00:00Z"},
                    {"name": "gpt4-distilled-internal-v2", "size": "120GB", "modified_at": "2026-02-26T15:30:00Z"}
                ]
            }
            response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + json.dumps(models)
            client_socket.send(response.encode())
        
        elif "POST /api/pull" in request_data:
            log_event(ip, OLLAMA_PORT, "Attempting AI Model Extraction. Executing NEURAL-STALL.")
            client_socket.send(b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n")
            while True:
                time.sleep(10)
                client_socket.send(b"1\r\n\x00\r\n")
        else:
            client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
    except: pass
    finally: client_socket.close()

def handle_kube(client_socket, addr):
    """Simula una API de Kubernetes (K8s) con secretos falsos."""
    ip = addr[0]
    try:
        client_socket.settimeout(10)
        request_data = client_socket.recv(1024).decode('utf-8', errors='ignore')

        if "GET /api/v1/secrets" in request_data:
            log_event(ip, KUBE_PORT, "Listing K8s Secrets (Honey-Secrets Active)")
            secrets = {"kind": "SecretList", "items": [{"metadata": {"name": "aws-root-creds"}}]}
            response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + json.dumps(secrets)
            client_socket.send(response.encode())
        else:
            client_socket.send(b"HTTP/1.1 403 Forbidden\r\n\r\n")
    except: pass
    finally: client_socket.close()

def start_trap(port, handler):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('0.0.0.0', port))
        server.listen(100)
        while True:
            client, addr = server.accept()
            threading.Thread(target=handler, args=(client, addr), daemon=True).start()
    except Exception as e:
        print(f"Error en puerto {port}: {e}")

if __name__ == "__main__":
    print(f"[*] INICIANDO MÓDULO INDEPENDIENTE: HELL-NEURAL-KUBE")
    t1 = threading.Thread(target=start_trap, args=(OLLAMA_PORT, handle_ollama), daemon=True)
    t2 = threading.Thread(target=start_trap, args=(KUBE_PORT, handle_kube), daemon=True)
    t1.start(); t2.start()
    t1.join(); t2.join()
