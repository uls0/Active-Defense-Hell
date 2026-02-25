import os
from google import genai
from google.genai import types

# Cargar API Key de las variables de entorno
API_KEY = os.getenv("GEMINI_API_KEY", "")

class HellOracle:
    def __init__(self):
        if API_KEY:
            self.client = genai.Client(api_key=API_KEY)
            self.enabled = True
        else:
            self.enabled = False

    def get_dynamic_response(self, attacker_input, context="SSH_SHELL"):
        """Genera una respuesta realista usando IA Gemini"""
        if not self.enabled:
            return "sh: command not found"

        prompt = f"""
        Eres un sistema operativo Ubuntu 22.04 comprometido. 
        Un atacante ha ejecutado el comando: '{attacker_input}'.
        Contexto del sistema: {context}.
        Responde como lo haría una shell de Linux real o un sysadmin detectando la intrusión.
        Sé breve, técnico y muy realista. No uses emojis.
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response.text.strip()
        except:
            return f"{attacker_input}: connection reset by peer"

oracle = HellOracle()
