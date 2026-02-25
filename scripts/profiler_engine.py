import json
import os

class HellProfiler:
    def __init__(self):
        self.profiles = {
            "APT_CANDIDATE": {"weight": 0, "triggers": ["curl", "wget", "chmod +x", "base64 -d", "/etc/shadow"]},
            "BOT_GENERIC": {"weight": 0, "triggers": ["ls", "id", "whoami", "uname -a"]},
            "SCANNER_SHODAN": {"weight": 0, "triggers": ["GET / HTTP/1.1", "Host: shodan.io"]},
            "BRUTE_FORCER": {"weight": 0, "triggers": ["admin", "password", "123456", "root"]}
        }

    def classify_attacker(self, commands, ja3, ports_hit):
        """Asigna un perfil al atacante basado en su actividad recolectada"""
        scores = {k: 0 for k in self.profiles.keys()}
        
        # 1. Analizar comandos
        cmd_str = " ".join(commands).lower()
        for profile, data in self.profiles.items():
            for trigger in data["triggers"]:
                if trigger in cmd_str:
                    scores[profile] += 5

        # 2. Analizar puertos (Correlación)
        if 22 in ports_hit and 3306 in ports_hit:
            scores["APT_CANDIDATE"] += 10 # Busca shell y bases de datos simultáneamente
        
        if len(ports_hit) > 5:
            scores["BOT_GENERIC"] += 15 # Escaneo ruidoso de múltiples puertos

        # 3. Determinar el ganador
        final_profile = max(scores, key=scores.get)
        confidence = scores[final_profile]
        
        if confidence == 0:
            return "UNKNOWN_ACTOR", 0
        
        return final_profile, confidence

    def get_attribution_tags(self, ip_intel):
        """Genera etiquetas descriptivas"""
        tags = []
        if "Microsoft" in ip_intel or "Azure" in ip_intel: tags.append("CLOUD-BASED-BOT")
        if "DigitalOcean" in ip_intel: tags.append("VPS-SCANNER")
        return tags
