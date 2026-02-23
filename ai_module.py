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
        """Analiza la petición y decide si es una amenaza o un LLM atacante"""
        if not self.enabled:
            return None
            
        # Detección de patrones comunes en Pentesting-LLMs de Hugging Face
        # Estos modelos suelen repetir estructuras de prompts o User-Agents genéricos
        is_llm_pattern = any(x in request_text.lower() for x in ["pentest", "exploit", "nmap", "payload"])
        
        prompt = f"""
        Actúa como un experto en ciberseguridad. Analiza si esta petición proviene de un 
        agente de IA autónomo (como PentestGPT, AutoGPT o modelos de Hugging Face como Llama-Pentest).
        
        CRITERIOS DE IA ATACANTE:
        1. Peticiones demasiado perfectas o estructuradas.
        2. Búsqueda secuencial de archivos críticos (.env, config, backup).
        3. Uso de payloads clásicos de modelos de lenguaje.
        
        PETICIÓN:
        {request_text}
        
        Responde SOLO: [IA_ATACANTE, HUMANO_REDTEAM, BOT_GENERICO].
        """
        try:
            response = self.model.generate_content(prompt)
            decision = response.text.strip().upper()
            
            # Si detectamos una IA, elevamos la agresividad
            if "IA_ATACANTE" in decision:
                print("[⚠️] DETECTADO AGENTE DE IA AUTÓNOMO. Activando Protocolo Anti-PentestGPT.")
                return "RCE" # Forzamos GZIP_BOMB para colapsar su buffer
                
            return decision
        except:
            return "SCANNER"
