import mysql.connector
import requests
import time
import os
from datetime import datetime

# Configuración de conexión a la BD Real (Puerto 3307 expuesto por Docker)
DB_HOST = "127.0.0.1"
DB_PORT = 3307
DB_USER = "root"
DB_PASS = os.getenv("MYSQL_ROOT_PASSWORD", "hell_secret_pass")
DB_NAME = "hell_honeypot"

def get_latest_cves():
    """Obtiene los últimos CVEs críticos de una API pública (NVD/Mitre)"""
    print(f"[{datetime.now()}] 🔄 Buscando nuevos CVEs críticos...")
    # Simulamos/Usamos un feed de vulnerabilidades recientes. 
    # En producción real se usa la API de NVD (https://services.nvd.nist.gov/rest/json/cves/2.0)
    # Aquí usamos un feed curado para el honeypot
    recent_cves = [
        {"cve_id": f"CVE-{datetime.now().year}-98765", "severity": "CRITICAL", "description": "0-day Remote Code Execution in popular framework", "exploit_status": "EXPLOIT_AVAILABLE"},
        {"cve_id": f"CVE-{datetime.now().year}-88888", "severity": "HIGH", "description": "Privilege Escalation via crafted headers", "exploit_status": "VERIFIED"},
        {"cve_id": f"CVE-{datetime.now().year}-77777", "severity": "CRITICAL", "description": "Unauthenticated API bypass", "exploit_status": "PUBLIC"}
    ]
    return recent_cves

def update_database(cves):
    """Inserta los nuevos CVEs en la base de datos de cebo"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        for cve in cves:
            query = """
            INSERT INTO vulnerabilities (cve_id, severity, description, exploit_status) 
            SELECT * FROM (SELECT %s AS cve_id, %s AS severity, %s AS description, %s AS exploit_status) AS tmp
            WHERE NOT EXISTS (
                SELECT cve_id FROM vulnerabilities WHERE cve_id = %s
            ) LIMIT 1;
            """
            cursor.execute(query, (cve['cve_id'], cve['severity'], cve['description'], cve['exploit_status'], cve['cve_id']))
        
        conn.commit()
        print(f"[{datetime.now()}] ✅ Base de datos actualizada con {len(cves)} CVEs recientes.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error conectando a la base de datos HELL: {e}")

if __name__ == "__main__":
    print("="*50)
    print(" 🕷️ HELL MODULE: CVE AUTO-UPDATER (Cebo Dinámico)")
    print("="*50)
    new_cves = get_latest_cves()
    update_database(new_cves)
