import os
import google.generativeai as genai

class GeminiDefender:
    def __init__(self, api_key):
        self.enabled = False
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.enabled = True
                print("[🤖] IA Gemini conectada y lista para defensa activa.")
            except Exception as e:
                print(f"[!] Fallo al conectar con Gemini: {e}")
        else:
            print("[i] No se proporcionó API Key. IA en modo pasivo.")

    def analyze_threat(self, request_text):
        """Analiza la petición y decide si es una amenaza"""
        if not self.enabled:
            return None # Fallback a reglas clásicas
            
        prompt = f"""
        Actúa como un experto en ciberseguridad forense. Analiza la siguiente petición HTTP 
        hecha a un honeypot y dime si es un escaneo automatizado, un intento de RCE, 
        o un humano curioso. Responde SOLO con una de estas categorías: 
        [SCANNER, RCE, DATA_LEAK, IGNORE].
        
        PETICIÓN:
        {request_text}
        """
        try:
            response = self.model.generate_content(prompt)
            decision = response.text.strip().upper()
            return decision
        except:
            return "SCANNER" # Decisión por defecto en fallo
