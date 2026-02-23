import os

def setup_hell_db():
    print("[🗄️] Configurando Base de Datos de CVEs Falsos...")
    
    # Generamos el SQL puro para ser importado en Docker/Portainer directamente
    schema = """
-- PROYECTO HELL: BASE DE DATOS DE CEBO
CREATE DATABASE IF NOT EXISTS hell_honeypot;
USE hell_honeypot;

CREATE TABLE IF NOT EXISTS vulnerabilities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cve_id VARCHAR(50),
    severity VARCHAR(20),
    description TEXT,
    exploit_status VARCHAR(50)
);

INSERT INTO vulnerabilities (cve_id, severity, description, exploit_status) VALUES
('CVE-2024-9999', 'CRITICAL', 'Remote Code Execution in Core System', 'AVAILABLE'),
('CVE-2023-1234', 'HIGH', 'SQL Injection in Admin Login', 'VERIFIED'),
('CVE-2021-35394', 'CRITICAL', 'Realtek SDK UDPServer Command Injection', 'PUBLIC');
    """
    
    sql_path = os.path.join("Proyectos_Activos", "HELL", "init_db.sql")
    with open(sql_path, "w") as f:
        f.write(schema)
    
    print(f"[✔] Archivo {sql_path} generado. Listo para importar en Docker.")

if __name__ == "__main__":
    setup_hell_db()
