import os

def generate_canary_pdf(target_ip, filename):
    """
    Genera un archivo PDF con un Canarytoken embebido que apunta a nuestro servidor.
    Cuando el atacante abre el PDF, su lector (Adobe, Chrome, etc.) intentará
    cargar un recurso remoto, avisándonos de su ubicación real.
    """
    tracking_url = f"http://{target_ip}/tracking/beacon.png?id={filename}"
    
    # Estructura mínima de un PDF con disparador de URL (URI Action)
    pdf_content = (
        f"%PDF-1.1
"
        f"1 0 obj << /Type /Catalog /Pages 2 0 R /OpenAction << /S /URI /URI ({tracking_url}) >> >> endobj
"
        f"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
"
        f"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >> endobj
"
        f"4 0 obj << /Length 50 >> stream
"
        f"BT /F1 24 Tf 100 700 Td (CONFIDENTIAL DOCUMENT - GRUPO MODELO) Tj ET
"
        f"endstream endobj
"
        f"xref
0 5
0000000000 65535 f
0000000010 00000 n
0000000079 00000 n
0000000138 00000 n
0000000212 00000 n
"
        f"trailer << /Size 5 /Root 1 0 R >>
"
        f"startxref
310
%%EOF"
    )
    return pdf_content.encode()

def serve_canary_file(client_socket, my_ip, filename):
    """Sirve el PDF envenenado al atacante"""
    print(f"[🕵️] Generando Canary PDF para carnada: {filename}")
    pdf_data = generate_canary_pdf(my_ip, filename)
    header = (
        "HTTP/1.1 200 OK
"
        "Content-Type: application/pdf
"
        f"Content-Disposition: attachment; filename="{filename}"
"
        f"Content-Length: {len(pdf_data)}
"
        "Connection: close

"
    )
    try:
        client_socket.send(header.encode() + pdf_data)
    except: pass
