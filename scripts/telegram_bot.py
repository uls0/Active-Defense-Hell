import requests
import os

class HellBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.enabled = True if token and chat_id else False

    def send_alert(self, message):
        """Envía una alerta de seguridad al canal de Telegram"""
        if not self.enabled: return
        
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": f"🔥 HELL ALERT 🔥

{message}",
            "parse_mode": "HTML"
        }
        try:
            requests.post(url, json=payload, timeout=5)
        except:
            pass

    def format_burnout_alert(self, ip, port, duration, data_mb, status):
        msg = (
            f"<b>Target Neutralized!</b>
"
            f"━━━━━━━━━━━━━━━━━━
"
            f"<b>IP:</b> <code>{ip}</code>
"
            f"<b>Port:</b> {port}
"
            f"<b>Retention:</b> {duration}s
"
            f"<b>Data Injected:</b> {data_mb}MB
"
            f"<b>Mitigation:</b> {status}"
        )
        self.send_alert(msg)

    def format_canary_alert(self, ip, filename):
        msg = (
            f"<b>🔔 CANARYTOKEN TRIGGERED!</b>
"
            f"━━━━━━━━━━━━━━━━━━
"
            f"<b>Real IP:</b> <code>{ip}</code>
"
            f"<b>File Opened:</b> {filename}
"
            f"<b>Location:</b> <a href='https://ip-api.com/#{ip}'>View on Map</a>"
        )
        self.send_alert(msg)
