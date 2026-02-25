import hashlib
import binascii

def get_ja3_hash(data):
    """
    Analiza un paquete TLS Client Hello y genera un hash JA3 simplificado.
    Estructura JA3: TLSVersion,Ciphers,Extensions,EllipticCurves,EllipticCurvePointFormats
    """
    try:
        # Verificar si es un Client Hello (0x16 0x03 ...)
        if data[0] != 0x16: return None
        
        # TLS Version (ej. 0x0303 para TLS 1.2)
        tls_version = int.from_bytes(data[9:11], 'big')
        
        # Session ID Length
        session_id_len = data[43]
        cipher_suite_start = 44 + session_id_len
        
        # Cipher Suites
        cipher_len = int.from_bytes(data[cipher_suite_start:cipher_suite_start+2], 'big')
        ciphers_raw = data[cipher_suite_start+2 : cipher_suite_start+2+cipher_len]
        ciphers = "-".join([str(int.from_bytes(ciphers_raw[i:i+2], 'big')) for i in range(0, len(ciphers_raw), 2)])
        
        # Generar string crudo para el hash
        # Nota: Por simplicidad en este emulador usamos Version y Ciphers
        ja3_string = f"{tls_version},{ciphers}"
        ja3_hash = hashlib.md5(ja3_string.encode()).hexdigest()
        
        return ja3_hash
    except:
        return "unknown_handshake"

def identify_client(ja3):
    """Mapeo conocido de huellas JA3 comunes"""
    signatures = {
        "771,4865-4866-4867-49195-49199": "Python-Requests/Urllib",
        "771,49195-49199-49196-49200": "Go-http-client",
        "771,49195-49196-52393-52392": "Curl/libcurl",
        "d85f3f16342c3008909350300ca3993b": "Metasploit Framework Bot",
        "de35424b3355054759bc4e0da3335e88": "Nmap NSE Engine"
    }
    return signatures.get(ja3, "Custom Bot/Unknown Tool")
