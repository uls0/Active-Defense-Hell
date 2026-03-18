import os

def generate_canary_pdf(my_server_ip, filename):
    """
    Genera un archivo PDF con un Canarytoken embebido.
    El tracking apunta de regreso a nuestro servidor HELL.
    """
    tracking_url = f"http://{my_server_ip}/tracking/beacon.png?id={filename}"
    
    pdf_content = f"""%PDF-1.1
1 0 obj << /Type /Catalog /Pages 2 0 R /OpenAction << /S /URI /URI ({tracking_url}) >> >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >> endobj
4 0 obj << /Length 50 >> stream
BT /F1 24 Tf 100 700 Td (CONFIDENTIAL DOCUMENT - MONEX FINANCIAL) Tj ET
endstream endobj
xref
0 5
0000000000 65535 f
0000000010 00000 n
0000000079 00000 n
0000000138 00000 n
0000000212 00000 n
trailer << /Size 5 /Root 1 0 R >>
startxref
310
%%EOF"""
    return pdf_content.encode()

def serve_canary_file(client_socket, my_server_ip, filename):
    """Sirve el PDF envenenado al atacante vía HTTP"""
    pdf_data = generate_canary_pdf(my_server_ip, filename)
    header = f"""HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="{filename}"
Content-Length: {len(pdf_data)}
Connection: close

"""
    try:
        client_socket.send(header.encode() + pdf_data)
        print(f"[🕵️] Canary Trap sent: {filename}")
    except: pass
