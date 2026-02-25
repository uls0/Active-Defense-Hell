import subprocess
import os

def apply_mss_clamping(ports, mss_value=64):
    """
    Usa iptables para forzar un MSS muy bajo en las conexiones entrantes.
    Esto obliga al atacante a enviar paquetes diminutos, aumentando su overhead.
    """
    if os.getuid() != 0:
        print("[!] Error: MTU Mismatching requiere privilegios de ROOT.")
        return False

    print(f"[🕸️] Aplicando TCP MSS Clamping ({mss_value} bytes) en puertos: {ports}")
    
    try:
        for port in ports:
            # Regla para forzar el MSS en paquetes SYN entrantes
            cmd = [
                "iptables", "-t", "mangle", "-A", "PREROUTING",
                "-p", "tcp", "--dport", str(port),
                "--tcp-flags", "SYN,RST", "SYN",
                "-j", "TCPMSS", "--set-mss", str(mss_value)
            ]
            subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print(f"[!] Error al aplicar iptables: {e}")
        return False

def cleanup_mss_rules(ports):
    """Limpia las reglas de mangle al cerrar el servidor"""
    if os.getuid() != 0: return
    
    print("[🧹] Limpiando reglas de red...")
    for port in ports:
        try:
            # Usamos -D para borrar la regla exacta
            subprocess.run([
                "iptables", "-t", "mangle", "-D", "PREROUTING",
                "-p", "tcp", "--dport", str(port),
                "--tcp-flags", "SYN,RST", "SYN",
                "-j", "TCPMSS", "--set-mss", "64"
            ], stderr=subprocess.DEVNULL)
        except: pass
