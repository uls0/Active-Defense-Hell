import requests
import os
import base64
import binascii

class VirusTotalReporter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.enabled = True if api_key else False

    def get_country(self, ip):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}?fields=country", timeout=5)
            if response.status_code == 200:
                return response.json().get('country', 'Unknown')
        except: pass
        return "Unknown"

    def report_ip(self, ip_address, scanner="Unknown", port=0, payload=b""):
        if not self.enabled: return
        country = self.get_country(ip_address)
        payload_hex = binascii.hexlify(payload[:32]).decode('utf-8') if payload else "None"
        report_text = (
            f"HELL ACTIVE DEFENSE REPORT\n---------------------------\n"
            f"Origin Country: {country}\nDetected Activity: Active Scanner / Vulnerability Probing\n"
            f"Target Port: {port}\nScanner Signature: {scanner}\nFirst Bytes Payload: {payload_hex}\n"
            f"Classification: Malicious Actor"
        )
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}/comments"
        headers = {"x-apikey": self.api_key, "Content-Type": "application/json"}
        try:
            requests.post(url, json={"data": {"type": "comment", "attributes": {"text": report_text}}}, headers=headers)
        except: pass

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
        """Consulta la API de IsMalicious con manejo de errores mejorado"""
        if not self.enabled: return {"score": 0, "is_malicious": False, "status": "Disabled"}
        url = "https://api.ismalicious.com/v1/check"
        headers = {"X-API-KEY": self.header_key, "Content-Type": "application/json"}
        try:
            response = requests.post(url, json={"query": ip_address}, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"score": 0, "is_malicious": False, "status": f"HTTP {response.status_code}"}
        except:
            return {"score": 0, "is_malicious": False, "status": "Connection Error"}
