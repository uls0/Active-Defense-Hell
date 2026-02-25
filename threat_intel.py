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

    def report_ip(self, ip_address, scanner="Unknown", port=0, payload=b"", location="Unknown", isp="Unknown"):
        if not self.enabled: return
        
        payload_hex = binascii.hexlify(payload[:32]).decode('utf-8') if payload else "None"
        report_text = (
            f"HELL ACTIVE DEFENSE REPORT\n---------------------------\n"
            f"Origin: {location}\nISP: {isp}\n"
            f"Target Port: {port}\nScanner: {scanner}\nPayload: {payload_hex}\n"
            f"Classification: Malicious Actor"
        )
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}/comments"
        headers = {"x-apikey": self.api_key, "Content-Type": "application/json"}
        try:
            requests.post(url, json={"data": {"type": "comment", "attributes": {"text": report_text}}}, headers=headers)
            print(f"[📡] Reporte enviado a VirusTotal para {ip_address}")
        except: pass

class AbuseIPDBReporter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.enabled = True if api_key else False
        self.url = 'https://api.abuseipdb.com/api/v2/report'

    def report_ip(self, ip_address, port, comment=""):
        if not self.enabled: return
        
        # Categorías de AbuseIPDB: 14 (Port Scan), 18 (Brute-Force), 21 (Web Spam), 22 (SSH)
        category = '14' # Default: Port Scan
        if port in [22, 2222]: category = '18,22'
        elif port in [80, 443, 8080]: category = '21'
        elif port == 445: category = '14,18'

        headers = {
            'Accept': 'application/json',
            'Key': self.api_key
        }
        data = {
            'ip': ip_address,
            'categories': category,
            'comment': f"HELL Honeypot: Malicious activity detected on port {port}. {comment}"
        }
        try:
            r = requests.post(self.url, headers=headers, data=data)
            if r.status_code == 200:
                print(f"[📡] IP {ip_address} reportada exitosamente a AbuseIPDB.")
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
        if not self.enabled: return {"score": 0, "is_malicious": False}
        url = "https://api.ismalicious.com/v1/check"
        headers = {"X-API-KEY": self.header_key, "Content-Type": "application/json"}
        try:
            response = requests.post(url, json={"query": ip_address}, headers=headers, timeout=5)
            return response.json() if response.status_code == 200 else None
        except: return None
