import requests
import os
import base64

class VirusTotalReporter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.enabled = True if api_key else False

    def report_ip(self, ip_address):
        """Registra la IP en VirusTotal mediante un comentario de comunidad"""
        if not self.enabled:
            return
            
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}/comments"
        headers = {
            "x-apikey": self.api_key,
            "Content-Type": "application/json"
        }
        data = {
            "data": {
                "type": "comment",
                "attributes": {
                    "text": f"🚨 [HELL HONEYPOT] IP detectada realizando ataques de RCE y escaneo de vulnerabilidades. Clasificada como: Atacante Activo. #honeypot #threatintel #active_defense"
                }
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                print(f"[📡] IP {ip_address} reportada exitosamente a VirusTotal.")
            else:
                print(f"[!] Error al reportar a VT: {response.status_code}")
        except Exception as e:
            print(f"[!] Fallo de conexión con VirusTotal: {e}")

class IsMaliciousReporter:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.enabled = True if api_key and api_secret else False
        if self.enabled:
            auth_string = f"{api_key}:{api_secret}"
            self.header_key = base64.b64encode(auth_string.encode()).decode()
        else:
            self.header_key = None

    def check_ip(self, ip_address):
        """Consulta si una IP es maliciosa en la API de IsMalicious"""
        if not self.enabled:
            return None
            
        url = "https://api.ismalicious.com/v1/check"
        headers = {
            "X-API-KEY": self.header_key,
            "Content-Type": "application/json"
        }
        data = {"query": ip_address}
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"[!] IsMalicious API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"[!] Fallo de conexión con IsMalicious: {e}")
            return None
