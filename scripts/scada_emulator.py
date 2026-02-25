import os
import time
import random

def handle_modbus_request(data):
    if len(data) < 7: return b""
    transaction_id = data[0:2]
    protocol_id = data[2:4]
    unit_id = data[6]
    function_code = data[7]

    if function_code == 3:
        payload = b"\x04\x04\x7e\x02\x58"
        response_len = len(payload) + 2
        header = transaction_id + protocol_id + response_len.to_bytes(2, 'big') + bytes([unit_id, function_code])
        return header + payload
    return b""

def scada_tarpit(client_socket):
    """Mantiene al atacante amarrado y rastrea bytes"""
    total_bytes = 0
    try:
        while True:
            chunk = os.urandom(2)
            client_socket.send(chunk)
            total_bytes += len(chunk)
            time.sleep(15)
    except: pass
    return total_bytes
