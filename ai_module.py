from google import genai
import os

class GeminiDefender:
    def __init__(self, api_key):
        self.enabled = False
        if api_key:
            try:
                # Nuevo SDK google-genai
                self.client = genai.Client(api_key=api_key)
                self.model_id = "gemini-1.5-flash"
                self.enabled = True
                print("[🤖] IA Gemini (New SDK) conectada y lista para defensa activa.")
            except Exception as e:
                print(f"[!] Fallo al conectar con Gemini: {e}")
        else:
            print("[i] No se proporcionó API Key. IA en modo pasivo.")

    def analyze_threat(self, request_text):
        """Analiza la petición y decide si es una amenaza o un LLM atacante"""
        if not self.enabled:
            return None
            
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
            # Nueva forma de generar contenido con google-genai
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            decision = response.text.strip().upper()
            
            if "IA_ATACANTE" in decision:
                print("[⚠️] DETECTADO AGENTE DE IA AUTÓNOMO. Activando Protocolo Anti-PentestGPT.")
                return "RCE"
                
            return decision
        except Exception as e:
            print(f"[!] Error en análisis de IA: {e}")
            return "SCANNER"
