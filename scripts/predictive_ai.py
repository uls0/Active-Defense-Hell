import time
import json
import os

class HellPredictiveAI:
    def __init__(self):
        self.history_file = "logs/attack_patterns.json"
        self.patterns = self.load_patterns()
        self.active_sessions = {} # {ip: [port1, port2, ...]}

    def load_patterns(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return {}

    def save_patterns(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.patterns, f, indent=4)

    def analyze_sequence(self, ip, new_port):
        """Registra la secuencia de puertos y predice el siguiente movimiento"""
        if ip not in self.active_sessions:
            self.active_sessions[ip] = []
        
        session = self.active_sessions[ip]
        if len(session) > 0:
            last_port = str(session[-1])
            # Crear o actualizar la probabilidad de transición
            if last_port not in self.patterns:
                self.patterns[last_port] = {}
            
            self.patterns[last_port][str(new_port)] = self.patterns[last_port].get(str(new_port), 0) + 1
            self.save_patterns()

        session.append(new_port)
        if len(session) > 5: session.pop(0) # Mantener ventana deslizante

        return self.predict_next(new_port)

    def predict_next(self, current_port):
        """Predice el puerto más probable basado en el historial global"""
        current_port = str(current_port)
        if current_port in self.patterns:
            transitions = self.patterns[current_port]
            # Retorna el puerto con más apariciones después del actual
            prediction = max(transitions, key=transitions.get)
            confidence = (transitions[prediction] / sum(transitions.values())) * 100
            if confidence > 40: # Umbral de confianza
                return int(prediction), confidence
        return None, 0
