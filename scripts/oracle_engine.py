import os
from google import genai
from google.genai import types

API_KEY = os.getenv("GEMINI_API_KEY", "")

class HellOracle:
    def __init__(self):
        self.enabled = True if API_KEY else False
        if self.enabled:
            self.client = genai.Client(api_key=API_KEY)
        self.sessions = {} # {ip: [history]}

    def get_dynamic_response(self, ip, attacker_input, context="SSH_SHELL"):
        """Genera una respuesta con memoria de sesión para máxima credibilidad"""
        if not self.enabled:
            return f"{attacker_input}: command not found"

        # Mantener historial por IP (últimos 10 mensajes)
        if ip not in self.sessions:
            self.sessions[ip] = []
        
        history = self.sessions[ip]
        self.sessions[ip].append(f"Attacker: {attacker_input}")
        if len(self.sessions[ip]) > 10: self.sessions[ip].pop(0)

        prompt = f"""
        Eres el kernel de un servidor Ubuntu 22.04 LTS corporativo bajo ataque.
        Tu objetivo es mantener al atacante conectado el mayor tiempo posible siendo extremadamente realista.
        
        HISTORIAL DE LA SESIÓN:
        {chr(10).join(history)}
        
        NUEVO COMANDO: '{attacker_input}'
        
        REGLAS:
        1. Responde EXACTAMENTE como lo haría una terminal de Linux.
        2. Si el comando es de escalación (sudo, su), inventa un error de 'System Policy' o 'Logged attempt'.
        3. Si el comando busca archivos (cat, grep), muestra fragmentos de archivos de configuración falsos pero técnicos.
        4. No uses emojis. No digas 'Hola'. Sé seco y profesional.
        5. Máximo 5 líneas de salida.
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            ai_text = response.text.strip()
            self.sessions[ip].append(f"System: {ai_text}")
            return ai_text
        except Exception as e:
            return f"{attacker_input}: internal system error (code {os.getpid()})"

oracle = HellOracle()
