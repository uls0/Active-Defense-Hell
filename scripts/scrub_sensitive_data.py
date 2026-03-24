import os
import re

FILES_TO_SCRUB = [
    "hell_core_hydra.py",
    "scripts/deploy_hydra_swarm.py",
    "scripts/setup_native_infra.py",
    "scripts/setup_secondary.py",
    "scripts/deploy_secondary_arsenal.py",
    "scripts/diagnose_mesh.py",
    "scripts/emergency_redeploy.py",
    "scripts/external_port_scan.py",
    "scripts/final_audit_sentinel.py",
    "scripts/final_fix_dashboard.py",
    "scripts/final_health_check.py",
    "scripts/find_loot.py",
    "scripts/forensic_elite_extraction.py",
    "scripts/forensic_incursion.py",
    "scripts/get_remote_report.py",
    "scripts/get_void_activity.py",
    "scripts/inject_native_loot.py",
    "scripts/inject_test_loot.py",
    "scripts/monitor_swarm.py",
    "scripts/native_audit_report.py",
    "scripts/poke_swarm_hydra.py",
    "scripts/restart_and_audit_hell.py",
    "scripts/simulate_report.py",
    "scripts/stress_test_lucifer.py",
    "scripts/threat_intel_auto.py",
    "scripts/threat_intel_hydra.py",
    "elite_deception.py"
]

PATTERNS = {
    r"178\.128\.72\.149": "os.getenv('PRO_IP')",
    r"170\.64\.151\.185": "os.getenv('SEC_IP')",
    r"INK0uJ8j4a5xCn": "os.getenv('PRO_PASS')",
    r"INK0uJ8j4a5xCR": "os.getenv('SEC_PASS')",
    r"MasterTv\.18a": "os.getenv('DB_PASS')",
    r"cf71ef8287e23566adc72ef2a5c519f0f542e66bfdacfcfc1ca3660fb5662279": "os.getenv('VT_API_KEY')",
    r"a294ad97c828dc6f8e5111d0209475ddbb3e984672d651688d3e3f9007c6a17520f2d20dc46974db": "os.getenv('ABUSE_API_KEY')"
}

def scrub_files():
    base_path = "C:/Users/UlisesGuzman/Documents/Proyectos/Gemini/Proyectos_Activos/HELL"
    for file_rel in FILES_TO_SCRUB:
        file_path = os.path.join(base_path, file_rel)
        if not os.path.exists(file_path): continue
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        for pattern, replacement in PATTERNS.items():
            # Envolver el reemplazo en comillas para que sea código Python válido
            content = re.sub(pattern, f'"{replacement}"', content)
        
        if content != original_content:
            if "import os" not in content:
                content = "import os\n" + content
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[✔] Saneado: {file_rel}")

if __name__ == "__main__":
    scrub_files()
