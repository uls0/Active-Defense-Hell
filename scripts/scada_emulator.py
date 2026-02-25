import os
import time
import random
import binascii

def handle_modbus_request(data):
    """
    Simula una RTU de CFE usando el protocolo Modbus TCP.
    Responde a consultas de registros con datos realistas de energía.
    """
    if len(data) < 7: return b""
    
    # Extraer campos de Modbus TCP
    transaction_id = data[0:2]
    protocol_id = data[2:4]
    length = data[4:6]
    unit_id = data[6]
    function_code = data[7]

    # Función 03: Read Holding Registers (Muy común en escaneo)
    if function_code == 3:
        # Responder con valores simulados de 115kV y 60Hz
        # Byte count: 4, Reg1: 1150 (0x047E), Reg2: 600 (0x0258)
        payload = b"\x04\x04\x7e\x02\x58"
        response_len = len(payload) + 2 # unit_id + func_code + payload
        header = transaction_id + protocol_id + response_len.to_bytes(2, 'big') + bytes([unit_id, function_code])
        return header + payload

    # Función 43: Get Device Identification (Aquí inyectamos la identidad CFE)
    if function_code == 43:
        identity = b"CFE-RTU-CUAUHTEMOC-01 [S/N: MX-7742]"
        header = transaction_id + protocol_id + (len(identity)+2).to_bytes(2, 'big') + bytes([unit_id, function_code])
        return header + identity

    return b""

def scada_tarpit(client_socket):
    """Mantiene al atacante de SCADA amarrado enviando goteo de registros"""
    while True:
        try:
            # Enviamos pequeñas fluctuaciones de voltaje cada 15 segundos
            client_socket.send(os.urandom(2))
            time.sleep(15)
        except: break
