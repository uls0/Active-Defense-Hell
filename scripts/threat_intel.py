import requests
import json
import os
import time

def analyze_ip(ip, vt_api_key):
    """Consulta la reputación de una IP en VirusTotal."""
    if not vt_api_key:
        return {"status": "error", "message": "No VT API Key"}

    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {
        "x-apikey": vt_api_key
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            stats = data['data']['attributes']['last_analysis_stats']
            reputation = data['data']['attributes']['reputation']
            
            # Guardar reporte en logs
            report_dir = "logs/intel_reports"
            os.makedirs(report_dir, exist_ok=True)
            report_path = os.path.join(report_dir, f"intel_{ip}.json")
            with open(report_path, "w") as f:
                json.dump(data, f, indent=4)
                
            return {
                "status": "success",
                "malicious": stats['malicious'],
                "suspicious": stats['suspicious'],
                "reputation": reputation,
                "verdict": "MALICIOUS" if stats['malicious'] > 0 else "CLEAN"
            }
        else:
            return {"status": "error", "message": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
