import socket
import ssl
import paramiko
import time
import json

HOST = "178.128.72.149"
SSH_PORT = 2200
USER = "root"
PASSWORD = "INK0uJ8j4a5xCn"

# Puertos a auditar (Muestra representativa de cada categoría)
ELITE_PORTS = {
    6443: ("K8s API", True),
    2376: ("Docker TLS", True),
    9100: ("Prometheus", False),
    9200: ("Elasticsearch", False),
    6379: ("Redis", False),
    8081: ("Shadow API", True),
    5000: ("Shadow API", True),
    8000: ("IA Inference", True),
    11434: ("Ollama/IA", False)
}

def audit_connectivity_and_banners():
    results = {}
    print(f"--- ESCANEANDO MEXCAPITAL EN {HOST} ---")
    
    for port, (name, is_ssl) in ELITE_PORTS.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            if is_ssl:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                with socket.create_connection((HOST, port), timeout=5) as s:
                    with context.wrap_socket(s, server_hostname="api-prod.mexcapital.com.mx") as ssock:
                        banner = f"SSL_OK | Cert Issued to MexCapital | Peer: {ssock.version()}"
            else:
                sock.connect((HOST, port))
                if port == 6379:
                    sock.sendall(b"PING\r\n")
                else:
                    sock.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
                
                banner = sock.recv(512).decode('utf-8', errors='ignore').strip().split('\n')[0]
                sock.close()
                
            results[port] = {"status": "OPEN", "name": name, "banner": banner}
        except Exception as e:
            results[port] = {"status": "CLOSED/FILTERED", "name": name, "error": str(e)}
            
    return results

def audit_remote_logs():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, SSH_PORT, USER, PASSWORD, timeout=15)
        
        commands = {
            "hell_activity": "tail -n 15 /root/Active-Defense-Hell/logs/hell_activity.log",
            "lucifer_mini": "tail -n 15 /root/Active-Defense-Hell/logs/lucifer_mini.log",
            "docker_health": "docker ps --format '{{.Names}}: {{.Status}}'"
        }
        
        log_results = {}
        for key, cmd in commands.items():
            stdin, stdout, stderr = ssh.exec_command(cmd)
            log_results[key] = stdout.read().decode('utf-8').strip()
            
        ssh.close()
        return log_results
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    network_report = audit_connectivity_and_banners()
    log_report = audit_remote_logs()
    
    final_output = {
        "network_audit": network_report,
        "remote_telemetry": log_report,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    }
    print(json.dumps(final_output, indent=2))
