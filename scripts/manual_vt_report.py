import requests
import json

IP = '204.76.203.56'
VT_KEY = 'cf71ef8287e23566adc72ef2a5c519f0f542e66bfdacfcfc1ca3660fb5662279'
COMMENT = 'HELL STORM: Confirmed Aeternum C2 node detected on port 8545. High-confidence botnet reconnaissance. Profile: Residential/Netherlands.'

headers = {
    "x-apikey": VT_KEY,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

print(f"[*] Reportando IP {IP} (Aeternum) con el nuevo motor STORM...")

try:
    comment_url = f"https://www.virustotal.com/api/v3/ip_addresses/{IP}/comments"
    comment_data = {
        "data": {
            "type": "comment",
            "attributes": {
                "text": COMMENT
            }
        }
    }
    
    c_res = requests.post(comment_url, json=comment_data, headers=headers, timeout=10)
    print(f"Resultado API: {c_res.status_code}")

    if c_res.status_code in [200, 201]:
        print("[✅] EXITO: Ya debe aparecer en uls0.")
    else:
        print(f"[❌] Fallo: {c_res.text}")

except Exception as e:
    print(f"[🔥] Error: {e}")
