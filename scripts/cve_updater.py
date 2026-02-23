import mysql.connector
import os
import time
from datetime import datetime

DB_HOST = "127.0.0.1"
DB_PORT = 3307
DB_USER = "root"
DB_PASS = os.getenv("MYSQL_ROOT_PASSWORD", "hell_secret_pass")
DB_NAME = "hell_honeypot"

def setup_table(cursor):
    """Crea la tabla vulnerabilities si no existe"""
    print("🛠️ Verificando/Creando estructura de tabla...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vulnerabilities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cve_id VARCHAR(50),
            severity VARCHAR(20),
            description TEXT,
            exploit_status VARCHAR(50)
        )
    """)

def update():
    print("="*50)
    print(" 🔄 HELL MODULE: CVE UPDATER (Self-Healing)")
    print("="*50)
    
    cves = [
        (f"CVE-{datetime.now().year}-1001", "CRITICAL", "Remote Exploit in Cloud Stack", "PUBLIC"),
        (f"CVE-{datetime.now().year}-2002", "HIGH", "Auth Bypass in Enterprise Portal", "EXPLOIT_AVAILABLE"),
        ("CVE-2021-35394", "CRITICAL", "Realtek SDK UDPServer Command Injection", "PUBLIC")
    ]

    conn = None
    for i in range(5):
        try:
            conn = mysql.connector.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS)
            if conn.is_connected(): break
        except:
            print(f"⌛ Esperando a que la DB despierte (Intento {i+1}/5)...")
            time.sleep(10)

    if not conn:
        print("❌ No se pudo conectar a la DB. Verifica el puerto 3307.")
        return

    try:
        cursor = conn.cursor()
        # Reparación automática
        setup_table(cursor)
        
        for cve in cves:
            cursor.execute("INSERT IGNORE INTO vulnerabilities (cve_id, severity, description, exploit_status) VALUES (%s, %s, %s, %s)", cve)
        
        conn.commit()
        print(f"✅ Base de datos verificada y actualizada con éxito.")
    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    update()
