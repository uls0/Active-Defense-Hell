import requests
import os
import base64
import binascii

class VirusTotalReporter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.enabled = True if api_key else False

    def get_country(self, ip):
        """Obtiene el país de la IP usando ip-api (gratuito)"""
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}?fields=country", timeout=5)
            if response.status_code == 200:
                return response.json().get('country', 'Unknown')
        except: pass
        return "Unknown"

    def report_ip(self, ip_address, scanner="Unknown", port=0, payload=b""):
        """Registra un reporte profesional en VirusTotal con metadatos forenses"""
        if not self.enabled:
            return
            
        country = self.get_country(ip_address)
        payload_hex = binascii.hexlify(payload[:32]).decode('utf-8') if payload else "None"
        
        # Formato profesional en lista
        report_text = (
            f"HELL ACTIVE DEFENSE REPORT\n"
            f"---------------------------\n"
            f"Origin Country: {country}\n"
            f"Detected Activity: Active Scanner / Vulnerability Probing\n"
            f"Target Port: {port}\n"
            f"Scanner Signature: {scanner}\n"
            f"First Bytes Payload: {payload_hex}\n"
            f"Classification: Malicious Actor"
        )

        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}/comments"
        headers = {
            "x-apikey": self.api_key,
            "Content-Type": "application/json"
        }
        data = {
            "data": {
                "type": "comment",
                "attributes": {
                    "text": report_text
                }
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                print(f"[📡] Reporte forense de {ip_address} enviado a VirusTotal.")
            else:
                print(f"[!] VT Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[!] Error al contactar VirusTotal: {e}")

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
        if not self.enabled:
            return None
        url = "https://api.ismalicious.com/v1/check"
        headers = { "X-API-KEY": self.header_key, "Content-Type": "application/json" }
        data = {"query": ip_address}
        try:
            response = requests.post(url, json=data, headers=headers, timeout=5)
            return response.json() if response.status_code == 200 else None
        except: return None
