import requests
import json
import os
import time

def analyze_ip(ip, vt_api_key):
    """Consulta la reputación de una IP en VirusTotal."""
    if not vt_api_key:
        return {"status": "error", "message": "No VT API Key"}

    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": vt_api_key}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            stats = data['data']['attributes']['last_analysis_stats']
            return {
                "status": "success",
                "malicious": stats['malicious'],
                "verdict": "MALICIOUS" if stats['malicious'] > 0 else "CLEAN"
            }
    except: pass
    return {"status": "error", "message": "Query failed"}

def report_ip_to_vt(ip, vt_api_key, comment_text):
    """
    Reporta activamente una IP a VirusTotal enviando un voto de 'malicious'
    y un comentario técnico. Esto aparecerá en el perfil del usuario.
    """
    if not vt_api_key: return False
    
    headers = {
        "x-apikey": vt_api_key,
        "Content-Type": "application/json"
    }

    # 1. Enviar Voto Malicioso
    vote_url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}/votes"
    vote_data = {
        "data": {
            "type": "vote",
            "attributes": {"verdict": "malicious"}
        }
    }
    
    # 2. Enviar Comentario Forense
    comment_url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}/comments"
    comment_data = {
        "data": {
            "type": "comment",
            "attributes": {"text": comment_text}
        }
    }

    try:
        # Votar
        requests.post(vote_url, json=vote_data, headers=headers, timeout=5)
        # Comentar
        r = requests.post(comment_url, json=comment_data, headers=headers, timeout=5)
        if r.status_code == 201 or r.status_code == 200:
            print(f"[🌐] IP {ip} reportada públicamente en VirusTotal.")
            return True
    except Exception as e:
        print(f"[❌] Error reportando a VT: {e}")
    
    return False
